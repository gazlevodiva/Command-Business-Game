window.onload = async function () {
  await updateOnlineDashboard();
  setInterval(updateOnlineDashboard, 3500);
};

let lastRollDiceActionId = 0

async function updateOnlineDashboard() {
  try {
    const response = await fetch("/dashboard_online/");
    const data = await response.json();

    const diceValueAction = data.game_actions.find(action => action.action_category === "DICE_VALUE");

    if( diceValueAction && lastRollDiceActionId !== diceValueAction.action_id){
      lastRollDiceActionId = diceValueAction.action_id;
      const parts = diceValueAction.action_name.split("-");
      const diceOne = parseInt(parts[0]);
      const diceTwo = parseInt(parts[1]);
      await rollTheDice( diceOne, diceTwo );      
    }    

    await updatePlayersInfo(data["players"]);

    await updateGameHistory(data["game_actions"]);

    await updateCommandBusiness(data["command_bank"], data["command_players"]);
  } catch (error) {
    console.error("Update Dashboard error:", error);
  }
}

function formatNumber(number) {
  const formatter = new Intl.NumberFormat("en-US");
  return formatter.format(number);
}
