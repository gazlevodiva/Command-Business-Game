
from game.methods.PlayerMethods import getSalary
from game.methods.PlayerMethods import setNewLevel
from game.methods.PlayerMethods import getInflation
from game.methods.PlayerMethods import getBusinesses
from game.methods.PlayerMethods import PlayerXReinvest

from game.methods.BusinessMethods import setCommandBusinessIncome
from game.methods.BusinessMethods import setPersonalBusinessIncome

from game.methods.NotificationModal import Modal

from game.views.player_panel import player_controller

from game.models.Moves import Moves
from game.models.Player import Player
from game.models.Actions import Actions

from game.decorators import check_user_session_hash


@check_user_session_hash
def new_level( request, session, player_id ):
    
    player = Player.objects.get( pk=player_id )

    # Make new move
    move = Moves.objects.create( player = player )

    Actions.objects.create(
        move     = move,
        name     = f"Перешел на { player.level+1 } круг.",
        count    = 0,
        category = 'NLWL',
    )

    # Create Bootstrap Modal window
    modal = Modal("Новый круг!", player)
    modal.type = "new_level"

    # 1 STEP - Inflation probability
    inflation_action = getInflation( move )
    modal.add_action( inflation_action )

    # 2 STEP - Get year salary
    salary_action = getSalary( move )
    modal.add_action( salary_action )

    # 3 STEP - Count business income or outcome
    for player_business in getBusinesses( player ):
       
        if player_business.is_command:
            business_actions = setCommandBusinessIncome( player_business, move )[3]

            for business_action in business_actions:
                modal.add_action( business_action )

        if not player_business.is_command:
            business_actions = setPersonalBusinessIncome( player_business, move )[3]

            for business_action in business_actions:
                modal.add_action( business_action )

    # 4 STEP - New level
    setNewLevel( player )

    # 5 STEP - player X reinvest his money to Command Business
    PlayerXReinvest( move=move )

    return player_controller.player_control( 
        request   = request, 
        player_id = player.id, 
        modal     = modal 
    )
