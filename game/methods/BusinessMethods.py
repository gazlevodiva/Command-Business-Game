from random import randint

from django.db.models import Sum

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions
from game.models.CommandPayments import CommandPayments
from game.models.BusinessPayments import BusinessPayments
from game.models.PlayersBusiness import PlayersBusiness
from game.models.PlayersBusinessStatus import PlayersBusinessStatus


def setDefoult(player_business, move):
    business = player_business.business

    # Defoult business will sale by 1/3 of cost
    business_sale_price = int(business.cost * 0.33)

    if player_business.is_command:
        CommandPayments.objects.create(
            count=business_sale_price,
            move=move,
        )

        name = f"🔥КБ {business.name} - Дефолт"

        defoult_action = Actions.objects.create(
            move=move,
            name=name,
            count=0,
            category="BSNS",
            is_command=True,
            is_personal=True,
            is_public=True,
        )

    if not player_business.is_command:
        name = f"Личный бизнес {business.name} - Дефолт"

        defoult_action = Actions.objects.create(
            move=move,
            name=name,
            count=business_sale_price,
            category="BSNS",
            visible=True,
            is_personal=True,
            is_public=False,
        )

    # Set business defoult
    player_business_status = PlayersBusinessStatus.objects.get(
        players_business=player_business
    )
    player_business_status.status = "DEFOULT"
    player_business_status.save()

    return defoult_action


def getBusinessProfit(player_business, move):
    # 1 STEP - Defoult Probability
    defoult_probability = randint(1, 16)
    # defoult_probability = 1

    # defoult_probability = 1
    if defoult_probability == 1:
        defoult_action = setDefoult(player_business, move)
        return (0, 0, 0, defoult_action)

    # 2 STEP - Rentability
    rentability = randint(
        player_business.business.min_rent, player_business.business.max_rent
    )

    # 3 STEP - Business Income
    profit = int(player_business.business.cost * rentability / 100)

    BusinessPayments.objects.create(
        move=move,
        player_business=player_business,
        count=profit,
        rentability=rentability,
        defoult_probability=defoult_probability,
        player_level=player_business.player.level + 1,
    )

    return (defoult_probability, rentability, profit, False)


def setPersonalBusinessIncome(player_business, move):
    # Business profit
    defoult, rentability, profit, defoult_action = getBusinessProfit(
        player_business, move
    )

    name = (
        f"Личный бизнес {player_business.business.name}, рент. {rentability}%"
    )
    payment_action = Actions.objects.create(
        move=move,
        name=name,
        count=profit,
        category="BSNS",
        is_personal=True,
        is_public=False,
    )

    actions = [payment_action]
    if defoult_action:
        actions.append(defoult_action)

    return (defoult, rentability, profit, actions)


def setCommandBusinessIncome(player_business, move):
    defoult, rentability, profit, defoult_action = getBusinessProfit(
        player_business, move
    )
    command_business_players = getCommandPlayers(player_business.player.game_session)

    # 20% after add to admin
    players_bank = int(profit * 0.8)
    admin_share = profit - players_bank
    admin_player = player_business.player

    payment_actions = []
    if defoult_action:
        payment_actions.append(defoult_action)

    if profit > 0:
        for command_player in command_business_players:
            # Players profit
            count = int(players_bank * command_player["share"] / 100)

            # Create move for every command player
            new_move = Moves.objects.create(
                player=command_player["move__player"], number=move.number
            )

            # Count new shares. Admin +20%
            if command_player["move__player"] == admin_player:
                count += admin_share
                name = f"КБ {player_business.business.name}, рент. {rentability}%"
                is_personal = True
                is_public = True
            else:
                name = f"Доход от КБ"
                is_personal = True
                is_public = False

            payment_action = Actions.objects.create(
                move=new_move,
                name=name,
                count=count,
                category="BSNS",
                is_command=True,
                is_personal=is_personal,
                is_public=is_public,
            )
            payment_actions.append(payment_action)

    if profit <= 0:
        name = f"КБ {player_business.business.name}, рент. {rentability}%"
        payment_action = Actions.objects.create(
            move=move,
            name=name,
            count=profit,
            category="BSNS",
            is_command=True,
            is_personal=True,
            is_public=True,
        )
        payment_actions.append(payment_action)

    return (defoult, rentability, profit, payment_actions)


def getCommandBank(game_session):
    return (
        CommandPayments.objects
        .filter(move__player__game_session=game_session)
        .aggregate(Sum("count"))
    )["count__sum"]


def getBusinessPayments(player_business):
    return (
        BusinessPayments.objects
        .filter(player_business=player_business)
    )


def getCommandPlayers(game_session):
    bank = (
        CommandPayments.objects.filter(move__player__game_session=game_session)
        .filter(category__in=["DEPOSITE", "WITHDRAW"])
        .aggregate(Sum("count"))
    )["count__sum"]

    player_payments = (
        CommandPayments.objects.filter(move__player__game_session=game_session)
        .filter(category__in=["DEPOSITE", "WITHDRAW"])
        .values("move__player")
        .annotate(share=Sum("count") * 100 / bank, count=Sum("count"))
        .order_by()
    )

    for player_payment in player_payments:
        player_payment["move__player"] = Player.objects.get(
            pk=player_payment["move__player"],
        )

    return player_payments


def getCommandShare(player):
    game_session = player.game_session

    command_players = getCommandPlayers(game_session=game_session)

    for command_player in command_players:
        if command_player["move__player"] == player:
            return (command_player["share"], command_player["count"])

    return (0, 0)


def sellCommandShare(move, sell_count=None):
    share, count = getCommandShare(move.player)

    name = f"Продал свою долю {share}% КБ за {count}"

    if sell_count:
        count = sell_count
        name = "Вывел средства из КБ"

    Actions.objects.create(
        move=move,
        name=name,
        count=count,
        category="CMND",
        is_command=True,
        is_personal=True,
        is_public=True,
    )

    CommandPayments.objects.create(
        move=move,
        category="WITHDRAW",
        count=-count
    )


def setVotion(move, business):
    players_business = PlayersBusiness.objects.create(
        player=move.player,
        business=business,
        is_command=True,
    )

    PlayersBusinessStatus.objects.create(
        players_business=players_business, move=move, status="VOTING"
    )

    Actions.objects.create(
        move=move,
        move_stage="CONTINUE",
        name="Начал голосование о покупке бизнеса",
        category="START_VOTE",
        visible=True,
        is_command=True,
        is_personal=True,
        is_public=True,
    )

    return {
        "move_id": move.id,
        "player_id": move.player.id,
        "business_id": players_business.business.id,
        "business_name": players_business.business.name,
        "business_cost": players_business.business.cost,
    }


def getVotion(move):
    move_actions = (
        Actions.objects
        .filter(move__player__game_session=move.player.game_session)
        .filter(move__number=move.number)
    )

    votion_started_action = move_actions.filter(category="START_VOTE")

    if move_actions.filter(category="START_VOTE").exists():
        votion_started_action = (
            move_actions
            .filter(category="START_VOTE")
            .first()
        )
    else:
        return False

    players_business_status = (
        PlayersBusinessStatus.objects
        .filter(move__player__game_session=move.player.game_session)
        .get(move__number=move.number)
    )

    # if players_business_status.status in ["ACTIVE", "UNVOTE"]:
    #     return False

    votes_actions = move_actions.filter(category__in=["VOTE_FOR", "VOTE_AGN"])

    # Add suggested player

    vote_for = 1
    vote_agn = 0
    votes = [
        {
            "player_id": votion_started_action.move.player.id,
            "category": "VOTE_FOR",
        },
    ]
    for vote in votes_actions:
        if vote.category == "VOTE_FOR":
            vote_for += 1

        if vote.category == "VOTE_AGN":
            vote_agn += 1

        votes.append(
            {
                "player_id": vote.move.player.id,
                "category": vote.category,
            }
        )

    business = players_business_status.players_business.business
    player = votion_started_action.move.player

    return {
        "move_id": votion_started_action.move.id,
        "player_id": player.id,
        "player_name": player.name,
        "business_id": business.id,
        "business_name": business.name,
        "business_cost": business.cost,
        "min_rent": business.min_rent,
        "max_rent": business.max_rent,
        "business_status": players_business_status.status,
        "votes": votes,
        "votes_for_count": vote_for,
        "votes_agn_count": vote_agn,
    }


def get_votion(move):
    move_actions = (
        Actions.objects
        .filter(move__player__game_session=move.player.game_session)
        .filter(move__number=move.number)
    )

    votion_started_action = move_actions.filter(category="START_VOTE")

    if move_actions.filter(category="START_VOTE").exists():
        votion_started_action = (
            move_actions
            .filter(category="START_VOTE")
            .first()
        )
    else:
        return False

    players_business_status = (
        PlayersBusinessStatus.objects
        .filter(move__player__game_session=move.player.game_session)
        .get(move__number=move.number)
    )

    # if players_business_status.status in ["ACTIVE", "UNVOTE"]:
    #     return False

    votes_actions = move_actions.filter(category__in=["VOTE_FOR", "VOTE_AGN"])

    # Add suggested player

    vote_for = 1
    vote_agn = 0
    votes = [
        {
            "player_id": votion_started_action.move.player.id,
            "category": "VOTE_FOR",
        },
    ]
    for vote in votes_actions:
        if vote.category == "VOTE_FOR":
            vote_for += 1

        if vote.category == "VOTE_AGN":
            vote_agn += 1

        votes.append(
            {
                "player_id": vote.move.player.id,
                "category": vote.category,
            }
        )

    business = players_business_status.players_business.business
    player = votion_started_action.move.player

    return {
        "def": "get_votion",
        "move_id": votion_started_action.move.id,
        "player_id": player.id,
        "player_name": player.name,
        "business_id": business.id,
        "business_name": business.name,
        "business_cost": business.cost,
        "min_rent": business.min_rent,
        "max_rent": business.max_rent,
        "business_status": players_business_status.status,
        "votes": votes,
        "votes_for_count": vote_for,
        "votes_agn_count": vote_agn,
    }


def setNewVote(move, player, category):
    votion = getVotion(move)
    voted_players = [x["player_id"] for x in votion["votes"]]

    # get player position, because it sa dont change
    player_move = Moves.objects.filter(player=player).last()

    if player.id in voted_players:
        return {
            "result": False,
            "desc": "Player already voted",
            "votion": votion
        }

    new_move = Moves.objects.create(
        number=move.number,
        position=player_move.position,
        player=player,
    )

    Actions.objects.create(
        move=new_move,
        move_stage="CONTINUE",
        name="Проголосовал",
        category=category,
        visible=False,
        is_command=True,
        is_personal=True,
        is_public=False,
    )

    # Set again
    votion = getVotion(move)
    voted_players = [x["player_id"] for x in votion["votes"]]
    session_players = playerIdForVotion(player.game_session)

    print("401:", voted_players, session_players)

    # If all players have voted
    if len(voted_players) == len(session_players):
        vote_for = 0
        vote_agn = 0

        for vote in votion["votes"]:
            if vote["category"] == "VOTE_FOR":
                vote_for += 1

            if vote["category"] == "VOTE_AGN":
                vote_agn += 1

        # Change player_business status
        votion_move = Moves.objects.get(pk=votion["move_id"])
        player_business_status = (
            PlayersBusinessStatus.objects
            .get(move=votion_move)
        )
        business = player_business_status.players_business.business

        if vote_for > vote_agn:
            Actions.objects.create(
                move=votion_move,
                move_stage="END",
                name=f"Стал администратором в {business.name}",
                is_command=True,
                is_personal=True,
                is_public=True,
            )

            CommandPayments.objects.create(
                move=votion_move,
                category="BUY_BIS",
                count=-business.cost
            )

            player_business_status.status = "ACTIVE"
            player_business_status.save()
            return {
                "result": True,
                "desc": "Player bought business",
                "votion": votion
            }

        else:
            Actions.objects.create(
                move=votion_move,
                move_stage="END",
                name="Не стал администратором",
                is_command=True,
                is_personal=True,
                is_public=True,
            )

            player_business_status.status = "UNVOTE"
            player_business_status.save()
            return {
                "result": False,
                "desc": "Player can not buy business",
                "votion": votion,
            }


def playerIdForVotion(game_session):
    command_players = getCommandPlayers(game_session)
    players = [
        player["move__player"].id
        for player in command_players
        if player["move__player"].visible
    ]
    return players


def player_id_for_votion(game_session):
    command_players = getCommandPlayers(game_session)
    players = [
        player["move__player"].id
        for player in command_players
        if player["move__player"].visible
    ]
    return players
