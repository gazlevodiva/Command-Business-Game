window.onload = async function () {
  await updateOnlineDashboard();
  setInterval(updateOnlineDashboard, 3500);
};

var lastRollDiceActionId = 0;
var fistPageUpdate = false;

async function updateOnlineDashboard() {
  try {
    const response = await fetch("/dashboard_online/");
    const data = await response.json();

    const diceValueAction = data.game_actions.find(action => action.action_category === "DICE_VALUE");

    console.log( fistPageUpdate )

    if( diceValueAction && lastRollDiceActionId !== diceValueAction.action_id && fistPageUpdate ){
      lastRollDiceActionId = diceValueAction.action_id;
      const parts = diceValueAction.action_name.split("-");
      const diceOne = parseInt(parts[0]);
      const diceTwo = parseInt(parts[1]);
      await rollTheDice( diceOne, diceTwo );      
    }    

    await updatePlayersInfo(data["players"]);

    await updateGameHistory(data["game_actions"]);

    await updateCommandBusiness(data["command_bank"], data["command_players"]);

    fistPageUpdate = true;

  } catch (error) {
    console.error("Update Dashboard error:", error);
  }
}

function formatNumber(number) {
  const formatter = new Intl.NumberFormat("en-US");
  return formatter.format(number);
}
