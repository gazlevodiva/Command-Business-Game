const gameHistoryDiv = document.getElementById("game_history");

async function updateGameHistory(gameActions) {
  if (parseInt(gameHistoryDiv.dataset.actionId) == gameActions[0].action_id) {
    return;
  }

  gameHistoryDiv.innerHTML = "";
  gameHistoryDiv.dataset.actionId = gameActions[0].action_id;

  let isFirstAction = true;
  let firstActionId = 0;
  let visibleActionsCount = 0;

  gameActions.forEach((action) => {

    if (visibleActionsCount == 6) {return}

    if (action.player_name !== "X" && action.action_visible) {
      var actionDiv = document.createElement("div");
      actionDiv.classList.add("fw-normal", "m-2");

      if (isFirstAction) {
        actionDiv.classList.add("h3", "mt-4", "mb-4");
        isFirstAction = false;

          if (action.action_id !== firstActionId){
            firstActionId = action.action_id;
            // Add animation
            actionDiv.classList.add("fade-in");
            actionDiv.addEventListener(
              "animationend",
              function () {
                actionDiv.classList.remove("fade-in");
                isFirstActionAnimated = true;
              },{ once: true } 
            );
          }        
      }

      var playerName = document.createElement("b");
      playerName.textContent = action.player_name + ": ";
      actionDiv.appendChild(playerName);

      var actionText = document.createElement("span");
      actionText.textContent = action.action_name;
      actionDiv.appendChild(actionText);

      if (action.action_count != 0) {
        var actionCount = document.createElement("span");
        actionCount.textContent = " " + formatNumber(action.action_count);

        if (action.action_count < 0) {
          actionCount.classList.add("text-danger");
        }

        if (action.action_count > 0) {
          actionCount.classList.add("text-success");
        }

        actionDiv.appendChild(actionCount);
      }
      gameHistoryDiv.appendChild(actionDiv);
      visibleActionsCount++;
    }
  });

  visibleActionsCount = 0
}
