from game.models.Moves import Moves
from game.models.Actions import Actions
from game.models.Business import Business

from game.models.Quiz import QuizQuestions
from game.models.Quiz import QuizAnswers

from game.models.PlayerQuiz import PlayerQuizQuestions
from game.models.PlayerQuiz import PlayerQuiz

import re
from random import sample, shuffle
from typing import List
from django.db.models import Subquery

from game.methods.BusinessMethods import get_business_payment_by_action
from game.methods.MoveMethods import get_move_actions
from django.db.models import QuerySet


def get_or_set_quiz(move):

    # Get all move actions
    move_actions = get_move_actions(move)

    # Check and try get quiz
    quiz_action, player_quiz = get_quiz(move_actions)

    if player_quiz.finished:
        return False

    # Get all business info
    businesses, business_actions, business_payments = (
        get_business_info_for_quiz(move_actions)
    )

    # Try to get Player quiz questions or create if not
    quiz_questions = QuizQuestions.objects.filter(
        playerquizquestions__quiz=player_quiz
    )

    if not quiz_questions:
        quiz_questions = generate_quiz_questions(
            businesses=[24],
            quiz_action=quiz_action,
            num_questions=5
        )

        for question in quiz_questions:
            PlayerQuizQuestions.objects.create(
                quiz=player_quiz,
                question=question,
            )

    # Make Dict or Json format of questions
    quiz_questions_fin = []
    for question in quiz_questions:

        answers = QuizAnswers.objects.filter(
            question=question
        ).values('id', 'name', 'is_correct')

        answers = list(answers)
        shuffle(answers)

        quiz_questions_fin.append({
            'question_id': question.id,
            'question_text': question.name,
            'answers': answers
        })

    # Finaly, make json answer
    res = {
        "player_quiz_id": player_quiz.id,
        "quiz_action_id": quiz_action.id,
        "quiz_questions": quiz_questions_fin,
        "businesses_id": [bus.id for bus in businesses],
        "business_actions_id": [ac.id for ac in business_actions],
        "business_payments_id": [ac.id for ac in business_payments],
    }
    return res


def get_quiz(move_actions):
    """
    Retrieves the quiz action and associated player
    quiz from a queryset of actions.

    Parameters:
        move_actions (QuerySet[Actions]): A queryset
        of action objects.

    Returns:
        tuple: A tuple containing the quiz action and the player quiz.
        If no existing player quiz is found, attempts to create one.

    This function first tries to find a quiz action of category
    'QUIZ' from the provided actions. If not found,
    it tries to set a new quiz action using the last action's move.
    It then checks if there is an ongoing player quiz
    for this action that isn't finished. If no such player quiz exists,
    it attempts to create one.
    """
    quiz_action = move_actions.filter(
        category="QUIZ"
    ).first()

    if not quiz_action:
        last_action = move_actions.last()

        if last_action:
            quiz_action = Actions.objects.create(
                move=last_action.move,
                name="Начал Викторину",
                category="QUIZ",
                is_personal=False,
                is_public=True,
            )

    player_quiz = PlayerQuiz.objects.filter(
        action=quiz_action,
    ).first()

    if not player_quiz:
        player_quiz = PlayerQuiz.objects.create(
            action=quiz_action,
            finished=False
        )

    return (quiz_action, player_quiz)


def generate_quiz_questions(businesses, quiz_action, num_questions):

    used_questions = PlayerQuizQuestions.objects.filter(
        quiz__action__move__player=quiz_action.move.player
    ).values_list(
        'question_id',
        flat=True
    )

    available_questions = QuizQuestions.objects.filter(
        business__in=businesses
    ).exclude(
        id__in=Subquery(used_questions)
    )

    count = min(num_questions, available_questions.count())
    if count == 0:
        return []

    res = sample(list(available_questions), k=count)
    return res


def finish_player_quiz(player_quiz):
    player_quiz.finished = True
    player_quiz.save()

    player_quiz.action.name = "Завершил викторину"
    player_quiz.action.save()


def can_create_quiz(actions):
    """
    Determines whether a new quiz can be created based
    on the following conditions:
    1. Presence of business actions with negative counts.
    2. Absence of unfinished quizzes linked to quiz actions.

    Parameters:
        actions (QuerySet[Action]): QuerySet of Action objects related
        to current player or game session.

    Returns:
        bool: True if a new quiz can be created, False otherwise.
    """
    # Check for any business actions with negative counts
    has_negative_business_actions = actions.filter(
        category="BSNS",
        count__lt=0
    ).exists()

    # Retrieve all quiz actions and check if there's an
    # unfinished PlayerQuiz associated with any
    quiz_actions = actions.filter(category="QUIZ")
    unfinished_quiz_exists = PlayerQuiz.objects.filter(
        action__in=quiz_actions,
        finished=False
    ).exists()

    # Return True if there are negative business actions and
    # no unfinished quizzes, otherwise False
    return has_negative_business_actions and (unfinished_quiz_exists or not quiz_actions.exists())


def get_business_info_for_quiz(actions):
    # Get all business actions with negative rentability
    business_actions = actions.filter(category="BSNS", count__lt=0)

    # Get business payments and businesses with negative rentability
    business_payments = []
    businesses = []
    for action in business_actions:
        business_payment = get_business_payment_by_action(action)
        business_payments.append(business_payment)
        businesses.append(business_payment.player_business.business)

    return businesses, business_actions, business_payments


def change_business_payment_by_quiz(actions):

    businesses, business_actions, business_payments = (
        get_business_info_for_quiz(actions)
    )

    for business_payment in business_payments:
        business_payment.rentability = 0
        business_payment.count = 0
        business_payment.save()

    for business_action in business_actions:
        new_action_name = re.sub(r'(-?\d+)(?=%)', '0', business_action.name)
        business_action.name = new_action_name
        business_action.count = 0
        business_action.save()
