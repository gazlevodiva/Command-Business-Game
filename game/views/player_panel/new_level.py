from game.methods.PlayerMethods import getSalary
from game.methods.PlayerMethods import getInflation
from game.methods.PlayerMethods import getBusinesses
from game.methods.PlayerMethods import PlayerXReinvest

from game.methods.BusinessMethods import setCommandBusinessIncome
from game.methods.BusinessMethods import setPersonalBusinessIncome

from game.models.Moves import Moves
from game.models.Actions import Actions


def is_new_level(player):
    player_move = Moves.objects.filter(player=player).last()
    player_last_actions = (
        Actions.objects
        .filter(move__player=player)
        .filter(move__number=player_move.number)
        .exclude(category="DICE_VALUE")
    )

    if not player_last_actions.filter(category="NLWL"):
        print("Player dont have any new_level actions.")
        return False

    if player_last_actions.filter(move_stage="END"):
        print("Player finish new_level move.")
        return False

    result = {
        "income": 0,
        "actions": [],
    }

    for action in player_last_actions.filter(visible=True):
        if action.is_personal:
            result["actions"].append(
                {
                    "name": action.name,
                    "count": action.count,
                }
            )
            result["income"] += action.count

    return result


# Actions for new level with CONTINUE
def set_new_level(move):
    Actions.objects.create(
        move=move,
        move_stage="CONTINUE",
        name=f"Перешел на { move.player.level+1 } круг",
        count=0,
        category="NLWL",
        visible=True,
        is_personal=True,
        is_public=True,
    )

    # ACTIONS
    actions = []

    # 1 STEP - Inflation probability
    inflation_action = getInflation(move)
    actions.append(inflation_action)

    # 2 STEP - Get year salary
    salary_action = getSalary(move)
    actions.append(salary_action)

    # 3 STEP - Count business income or outcome
    for player_business in getBusinesses(move.player):
        if player_business.is_command:
            business_actions = (
                setCommandBusinessIncome(player_business, move)[3]
            )

            for business_action in business_actions:
                actions.append(business_action)

        if not player_business.is_command:
            business_actions = (
                setPersonalBusinessIncome(player_business, move)[3]
            )

            for business_action in business_actions:
                actions.append(business_action)

    # 4 STEP - New level
    move.player.level += 1
    move.player.save()

    # 5 STEP - player X reinvest his money to Command Business
    PlayerXReinvest(move=move)
