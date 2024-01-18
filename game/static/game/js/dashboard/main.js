window.onload = async function () {
  await updateOnlineDashboard();
  setInterval(updateOnlineDashboard, 3500);
};

var lastRollDiceActionId = 0;
var fistPageUpdate = false;

async function updateOnlineDashboard() {
  let data = await getDashboardData();
  const diceValueAction = data.game_actions.find(action => action.action_category === "DICE_VALUE");

  if( diceValueAction && lastRollDiceActionId !== diceValueAction.action_id ){
    lastRollDiceActionId = diceValueAction.action_id;

    if ( fistPageUpdate ){
      const parts = diceValueAction.action_name.split("-");
      const diceOne = parseInt(parts[0]);
      const diceTwo = parseInt(parts[1]);
      await rollTheDice( diceOne, diceTwo );
    }    
  }

  await updateGameHistory(data.game_actions, data.votion);

  await updateCommandBusiness(data.command_bank, data.command_players);

  await updatePlayersInfo(data.players);

  fistPageUpdate = true;

}


async function getDashboardData() {
  try {
    const response = await fetch("/dashboard_online/");
    const data = await response.json();
    return data;

  } catch (error) {
    console.error("Update Dashboard error:", error);
  }
}

function formatNumber(number) {
  const formatter = new Intl.NumberFormat("en-US");
  return formatter.format(number);
}
