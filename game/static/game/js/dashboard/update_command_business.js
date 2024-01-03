const command_bank = document.getElementById("command_bank");
const commandPlayersDiv = document.getElementById("command_players");

async function updateCommandBusiness(commandBank, commandPlayers) {
  if (command_bank.innerText !== formatNumber(commandBank)) {
    command_bank.innerText = formatNumber(commandBank);

    commandPlayersDiv.innerHTML = "";
    commandPlayers.forEach((commandPlayer) => {
      if (commandPlayer.count > 0) {
        var rowDiv = document.createElement("div");
        rowDiv.className = "row";

        var colNameDiv = document.createElement("div");
        colNameDiv.className = "col-6 h5";
        colNameDiv.textContent = commandPlayer.name;

        var colShareDiv = document.createElement("div");
        colShareDiv.className = "col-2 h5";
        colShareDiv.textContent = commandPlayer.name + "%";

        
        rowDiv.appendChild(colNameDiv);
        rowDiv.appendChild(colShareDiv);        
        commandPlayersDiv.appendChild(rowDiv);
      }
    });
  }
}
