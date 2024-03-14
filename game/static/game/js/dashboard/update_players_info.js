const playersListDiv = document.getElementById("players_list");

let currentPlayerTurnId = 0;

async function updatePlayersInfo(players) {
  const newCurrentPlayerTurnId = players.find((player) => player.is_turn)?.id;

  players.forEach((player) => {
    updatePlayerCardOnGameTable(player); // update_players_card.js
  });

  currentPlayerTurnId = newCurrentPlayerTurnId;
  playersListDiv.innerHTML = "";

  players.forEach((player) => {
    const playerElement = createPlayerElement(player);
    playersListDiv.appendChild(playerElement);
  });
}

function createPlayerElement(player) {
  const playerElement = document.createElement("div");
  playerElement.classList.add("player-info-card");

  const rowElement = document.createElement("div");
  rowElement.classList.add("row");

  if (player.is_turn) {
    rowElement.classList.add("current-turn");
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
  iconElement.classList.add("player-info-icon-element");

  const icon = document.createElement("div");
  icon.style.margin = "0";
  icon.style.fontSize = "2vw";
  icon.textContent = player.icon;
  icon.classList.add("text-center");
  iconElement.appendChild(icon);

  const levelDiv = document.createElement("div");
  iconElement.classList.add("player-info-level-element");
  levelDiv.classList.add("text-muted", "text-center");
  levelDiv.textContent = player.level + " круг";
  iconElement.appendChild(levelDiv);

  return iconElement;
}

function createInfoElement(player) {
  const infoElement = document.createElement("div");
  infoElement.classList.add(
    "col-8",
    "d-flex",
    "flex-column",
    "justify-content-center",
  ); 

  const playerNameElement = createPlayerNameElement(player);
  infoElement.appendChild(playerNameElement);

  const balanceElement = createBalanceElement(player);
  infoElement.appendChild(balanceElement);

  if(player.businesses.length > 0){
  const businessesCountElement = createBusinessesCountElement(player);
  infoElement.appendChild(businessesCountElement);
  }

  return infoElement;
}

function createPlayerNameElement(player) {
  const playerNameElement = document.createElement("a");

  playerNameElement.classList.add("player-info-name-element");
  playerNameElement.classList.add("card-title");
  playerNameElement.classList.add("text-muted", "text-decoration-none", "text-break");

  playerNameElement.href = "/player_control_" + player.id + "/";
  playerNameElement.textContent = player.name;

  return playerNameElement;
}

function createBusinessesCountElement(player) {
  const businessesCountElement = document.createElement("div");

  businessesCountElement.classList.add("player-info-business-element");
  businessesCountElement.classList.add("text-muted");

  const defaultBusinesses = player.businesses
    .filter(business => business.status === "DEFOULT")
    .map(() => '🔥')
    .join('');

  const activeBusinesses = player.businesses
    .filter(business => business.status === "ACTIVE")
    .map(() => '🏦')
   .join('');

  businessesCountElement.textContent = defaultBusinesses + activeBusinesses;

  businessesCountElement.textContent = '🏦'.repeat(10);
  return businessesCountElement;
}

function createBalanceElement(player) {
  const balanceElement = document.createElement("div");

  balanceElement.classList.add("player-info-balance-element");
  balanceElement.textContent = formatNumber(player.balance);

  if (player.balance < 0) {
    balanceElement.classList.add("text-danger");
  }

  return balanceElement;
}
