const command_bank = document.getElementById("command_bank");
const commandPlayersDiv = document.getElementById("command_players");

async function updateCommandBusiness(commandBank, commandPlayers) {
  if (command_bank.innerText !== formatNumber(commandBank)) {

    command_bank.innerText = formatNumber(commandBank);
    if (commandBank < 0) {
      command_bank.classList.add("text-danger");
    } else {
      command_bank.classList.remove("text-danger");
    }

    commandPlayersDiv.innerHTML = "";
    commandPlayers.forEach((commandPlayer) => {
      if (commandPlayer.count > 0) {
        var rowDiv = document.createElement("div");
        rowDiv.classList.add("row");
        rowDiv.classList.add("mt-2");
        rowDiv.classList.add("mb-2");
        rowDiv.classList.add("player-info-command-card");

        var colNameDiv = document.createElement("div");
        colNameDiv.classList.add("col-4");
        colNameDiv.classList.add("text-muted");
        colNameDiv.classList.add("player-info-name-element");
        colNameDiv.textContent = commandPlayer.name;

        var colShareDiv = document.createElement("div");
        colShareDiv.classList.add("col-2");
        colShareDiv.textContent = commandPlayer.share + "%";
        if (commandPlayer.share < 1) {
          colShareDiv.textContent = "~1%";
        } else {
          colShareDiv.textContent = commandPlayer.share + "%";
        }

        var colBusinessDiv = document.createElement("div");
        // colBusinessDiv.classList.add("col-4");
        colBusinessDiv.classList.add("text-muted");
        colBusinessDiv.classList.add("player-info-business-element");
        const defaultBusinesses = commandPlayer.businesses
          .filter(business => business.status === "DEFOULT")
          .map(() => '🔥')
          .join('');

        const activeBusinesses = commandPlayer.businesses
          .filter(business => business.status === "ACTIVE")
          .map(() => '🏦')
          .join('');

        colBusinessDiv.textContent = defaultBusinesses + activeBusinesses;
        // colBusinessDiv.textContent = '🏦'.repeat(10); // normal for 7 biz

        rowDiv.appendChild(colNameDiv);
        rowDiv.appendChild(colShareDiv);
        rowDiv.appendChild(colBusinessDiv);  
        commandPlayersDiv.appendChild(rowDiv);
      }
    });
  }
}
