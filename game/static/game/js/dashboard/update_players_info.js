const playersListDiv = document.getElementById("players_list");

let currentPlayerTurnId = 0;

async function updatePlayersInfo(players) {
  const newCurrentPlayerTurnId = players.find((player) => player.is_turn)?.id;

  players.forEach((player) => {
    updatePlayerCardOnGameTable(player); // update_players_card.js
  });

  // if (currentPlayerTurnId === newCurrentPlayerTurnId) {
  //   return;
  // }

  currentPlayerTurnId = newCurrentPlayerTurnId;
  playersListDiv.innerHTML = "";

  players.forEach((player) => {
    const playerElement = createPlayerElement(player);
    playersListDiv.appendChild(playerElement);
  });
}

function createPlayerElement(player) {
  const playerElement = document.createElement("div");
  playerElement.classList.add("mb-3");

  const rowElement = document.createElement("div");
  rowElement.classList.add("row");

  if (player.is_turn) {
    rowElement.classList.add("current-turn", "m-4");
  }

  const iconElement = createIconElement(player);
  rowElement.appendChild(iconElement);

  const infoElement = createInfoElement(player);
  rowElement.appendChild(infoElement);

  playerElement.appendChild(rowElement);
  return playerElement;
}

function createIconElement(player) {
  const iconElement = document.createElement("div");
  iconElement.classList.add(
    "col-4",
    "d-flex",
    "flex-column",
    "justify-content-center"
  );

  const icon = document.createElement("div");
  icon.style.margin = "0";
  icon.style.fontSize = "45px";
  icon.textContent = player.icon;
  icon.classList.add("text-center");
  iconElement.appendChild(icon);

  const levelDiv = document.createElement("div");
  levelDiv.classList.add("text-muted", "text-center");
  levelDiv.textContent = player.level + " круг";
  iconElement.appendChild(levelDiv);

  return iconElement;
}

function createInfoElement(player) {
  const infoElement = document.createElement("div");
  infoElement.classList.add("col-6");

  const playerNameElement = createPlayerNameElement(player);
  infoElement.appendChild(playerNameElement);

  const balanceElement = createBalanceElement(player);
  infoElement.appendChild(balanceElement);

  const businessesCountElement = createBusinessesCountElement(player);
  infoElement.appendChild(businessesCountElement);

  return infoElement;
}

function createPlayerNameElement(player) {
  const playerNameElement = document.createElement("a");

  playerNameElement.classList.add("card-title");
  playerNameElement.classList.add("text-dark", "text-decoration-none");
  playerNameElement.classList.add("fs-4");

  playerNameElement.href = "/player_control_" + player.id + "/";
  playerNameElement.textContent = player.name;

  return playerNameElement;
}

function createBusinessesCountElement(player) {
  const businessesCountElement = document.createElement("div");
  businessesCountElement.classList.add("text-muted");
  businessesCountElement.classList.add("h5");
  // businessesCountElement.textContent = "Бизнесов: " + player.businesses.length;

  if ( player.businesses.length > 0 ){
    businessesCountElement.textContent = '🏦'.repeat(player.businesses.length);
  }

  return businessesCountElement;
}

function createBalanceElement(player) {
  const balanceElement = document.createElement("div");
  balanceElement.classList.add("fs-4");
  balanceElement.textContent = formatNumber(player.balance);

  if (player.balance < 0) {
    balanceElement.classList.add("text-danger");
  }

  return balanceElement;
}
