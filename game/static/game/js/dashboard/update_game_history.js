const gameHistoryDiv = document.getElementById("game_history");

// Like globals
var current_votion_active = false;
var current_votion_move_id = 0;
var current_votion_votes_count = 0;


var first_game_history_action_id = 0;
var first_game_history_action_id_animated = false;


async function updateGameHistory(gameActions, votion) {

  // Try to find votion
  const votion_action = gameActions.find(action => 
    action.action_id !== votion.action_id
  );

  if(votion_action && votion && votion.business_status == "VOTING"){
    current_votion_active = true;
    current_votion_move_id = votion.move_id;
  }else{
    current_votion_active = false;
    current_votion_move_id = 0;
    current_votion_votes_count = 0
  }

  // Get first action
  const new_first_action = gameActions.find(action => 
    action.player_name !== "X" && action.action_visible
  );
 
  // If first acton not changed and we don`t have active votion, dont change history
  if (new_first_action && first_game_history_action_id == new_first_action.action_id ) {
    if(!current_votion_active || current_votion_votes_count == votion.votes.length){
      return;
    }
  }

  // If votion has new votes, change it
  current_votion_votes_count = current_votion_active ? votion.votes.length : 0; 

  // If we have a new action, change action id and set animation to off
  first_game_history_action_id = new_first_action ? new_first_action.action_id : 0;
  first_game_history_action_id_animated = false;

  // Clear history to update
  gameHistoryDiv.innerHTML = "";

  // Set-up end flag
  let actionIndex = 0;
  gameActions.forEach((action) => {

    // Counter flag for 6 actions
    if(actionIndex == 8) {return}    

    // Lets print all actions
    if(action.player_name !== "X" && action.action_visible) {
      
      var actionDiv = document.createElement("div");
      actionDiv.classList.add("fw-normal", "m-2");

      // If first action
      if(actionIndex == 0) {
        actionDiv.classList.add("h3", "mt-4", "mb-4");     
        
        // If first action not animated -> animate
        if(!first_game_history_action_id_animated){
          fadeInAnimation(actionDiv); // Add fade-in animation
          first_game_history_action_id_animated = true; // Set that this action animated
        }

      }

      var playerName = document.createElement("b");
      playerName.textContent = action.player_name + ": ";
      actionDiv.appendChild(playerName);

      var actionText = document.createElement("span");
      

      if(current_votion_active && action.move_id == current_votion_move_id){
        actionText.textContent = `
        Начал голосование за покупку 
        ${votion.business_name} за 
        ${formatNumber(votion.business_cost)} 
        ✅ ${votion.votes_for_count} / ${votion.votes_agn_count} ❌
        `;
      } else {
        actionText.textContent = action.action_name;
      }
      actionDiv.appendChild(actionText);

      if (action.action_count != 0) {
        var actionCount = document.createElement("span");
        actionCount.textContent = " " + formatNumber(action.action_count);
        if (action.action_count < 0){actionCount.classList.add("text-danger");}
        if (action.action_count > 0){actionCount.classList.add("text-success");}
        actionDiv.appendChild(actionCount);
      }
      
      gameHistoryDiv.appendChild(actionDiv);
      actionIndex++;
    }

  });
  actionIndex = 0;
}


function fadeInAnimation(actionDiv){
  actionDiv.classList.add("fade-in");
  actionDiv.addEventListener("animationend", function () {
     actionDiv.classList.remove("fade-in");       
  },{ once: true } );
}
