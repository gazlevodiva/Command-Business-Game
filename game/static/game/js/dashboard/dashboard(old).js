const playersListDiv    = document.getElementById("players_list");
const gameHistoryDiv    = document.getElementById("game_history");
const command_bank      = document.getElementById("command_bank");
const commandPlayersDiv = document.getElementById("command_players");
const GameField         = document.getElementById("game_field");

const rollTheDiceGame = document.getElementById('rollthedice');
const elDiceOne = document.getElementById('dice1');
const elDiceTwo = document.getElementById('dice2');
let currentPlayerTurnId = null;

function formatNumber(number) {
  const formatter = new Intl.NumberFormat('en-US');
  return formatter.format(number);
}


async function updateOnlineDashboard() {
  try {
    const response = await fetch('/dashboard_online/');
    if (!response.ok) {
      throw new Error('Network response was not ok.');
    }
    const data = await response.json();

    updatePlayersInfo(data['players']);

    updateGameHistory(data['game_actions']);

    updateCommandBusiness(data['command_bank'], data['command_players']);

    


  } catch (error) {
    console.error('Ошибка при обновлении доски онлайн:', error);
  }
}


function updateGameHistory(gameActions) {

  // If last asctions have no difference? return
  var last_action_move = gameActions[0].move_number;
  var last_action_id   = gameActions[0].action_id;


  // if( parseInt(gameHistoryDiv.dataset.moveNumber) == last_action_move ){return}
  if( parseInt(gameHistoryDiv.dataset.actionId) == last_action_id ){return}

  gameHistoryDiv.innerHTML = '';
  // gameHistoryDiv.dataset.moveNumber = last_action_move;
  gameHistoryDiv.dataset.actionId   = last_action_id;
  
  let isFirstAction = true;

  gameActions.forEach(action => {
    if (action.player_name !== 'X' && action.action_visible) {
      var actionDiv = document.createElement("div");
      actionDiv.classList.add("fw-normal", 'm-2');

      if (isFirstAction) {
        actionDiv.classList.add("h3", "mt-4", "mb-4");

        actionDiv.classList.add('fade-in');

        actionDiv.addEventListener('animationend', function() {
          actionDiv.classList.remove('fade-in');
        }, { once: true });

        isFirstAction = false;  // Сбрасываем флаг после обработки первого действия
      }

      var playerName = document.createElement("b");
      playerName.textContent = action.player_name+': ';
      actionDiv.appendChild(playerName);

      var actionText = document.createElement("span");
      actionText.textContent = action.action_name;
      actionDiv.appendChild(actionText);

      if ( action.action_count != 0 ){
        var actionCount = document.createElement("span");
        actionCount.textContent = ' '+action.action_count; 

        if ( action.action_count < 0 ){
          actionCount.classList.add("text-danger");
        }

        if ( action.action_count > 0 ){
          actionCount.classList.add("text-success");
        }

        actionDiv.appendChild(actionCount);
      } 
      gameHistoryDiv.appendChild(actionDiv);

    }
  });
}


function updateCommandBusiness(commandBank, commandPlayers) {
  if (command_bank.innerText !== formatNumber(commandBank)) {
    command_bank.innerText = formatNumber(commandBank);
    
    commandPlayersDiv.innerHTML = '';
    commandPlayers.forEach(commandPlayer => {
      if (commandPlayer['share'] > 0) {
        var rowDiv = document.createElement("div");
        rowDiv.className = "row";

        var colNameDiv = document.createElement("div");
        colNameDiv.className = "col-6 h5";
        colNameDiv.textContent = commandPlayer['name'];

        var colShareDiv = document.createElement("div");
        colShareDiv.className = "col-2 h5";
        colShareDiv.textContent = commandPlayer['share'] + "%";

        rowDiv.appendChild(colNameDiv);
        rowDiv.appendChild(colShareDiv);
                
        commandPlayersDiv.appendChild(rowDiv);
      }
    });
  }
}


function updatePlayersInfo(players) {

  const newCurrentPlayerTurnId = players.find(player => player.is_turn)?.id;

  players.forEach(player => {
    updatePlayerCardOnGameTable(player);
  });

  if (currentPlayerTurnId === newCurrentPlayerTurnId) {return}
  currentPlayerTurnId = newCurrentPlayerTurnId;

  playersListDiv.innerHTML = '';

  players.forEach(player => {
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
  iconElement.classList.add("col-4", "d-flex", "flex-column", "justify-content-center");

  const icon = document.createElement("div");
  icon.style.margin = "0";
  icon.style.fontSize = "45px";
  icon.textContent = player.icon;
  icon.classList.add('text-center');
  iconElement.appendChild(icon);

  const levelDiv = document.createElement('div');
  levelDiv.classList.add('text-muted', 'text-center');
  levelDiv.textContent = player.level + ' круг';
  iconElement.appendChild(levelDiv);

  return iconElement;
}


function createInfoElement(player) {
  const infoElement = document.createElement("div");
  infoElement.classList.add("col-6");

  const playerNameElement = createPlayerNameElement(player);  
  infoElement.appendChild(playerNameElement);

  const businessesCountElement = createBusinessesCountElement(player);
  infoElement.appendChild(businessesCountElement);

  const balanceElement = createBalanceElement(player);
  infoElement.appendChild(balanceElement);

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
  businessesCountElement.textContent = "Бизнесов: " + player.businesses.length;

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


function animateMovement(element, oldRect, newRect, callback) {
  // Подготовка элемента к анимации
  element.style.position = 'absolute';
  element.style.left = oldRect.left + 'px';
  element.style.top = oldRect.top + 'px';

  // Анимация перемещения
  element.animate([
    { transform: 'translate(0, 0)' },
    { transform: `translate(${newRect.left - oldRect.left}px, ${newRect.top - oldRect.top}px)` }
  ], {
    duration: 1000, // Продолжительность анимации
    fill: 'forwards'
  }).onfinish = callback; // Вызов callback после завершения анимации
}


async function updatePlayerCardOnGameTable(player) {
  const playerCard = document.getElementById("player-" + player.id);

  if (playerCard) {
    const oldPlayerCardCellNumber = parseInt(playerCard.parentElement.id.split('-')[1]);
    
    if (oldPlayerCardCellNumber !== player.current_position) {

      const newPlayerCell = document.getElementById( "cell-" + player.current_position );
      let   newPlayerCard = createPlayerCard( player );

      newPlayerCard.style.visibility = 'hidden';

      // Получаем координаты старой и новой позиции
      const oldRect = playerCard.getBoundingClientRect();
      const newRect = newPlayerCard.getBoundingClientRect();

      playerCard.animate([
        { transform: 'translate(0, 0)' },
        { transform: `translate(${newRect.left - oldRect.left}px, ${newRect.top - oldRect.top}px)` }
      ], {
        duration: 1000,
        fill: 'forwards'
      }).onfinish = () => {
        // По завершении анимации добавляем карточку в новую ячейку и удаляем старую
        // newPlayerCell.appendChild(playerCard);
        playerCard.style.position = '';
        playerCard.style.left = '';
        playerCard.style.top = '';
        playerCard.remove();
        newPlayerCard.style.visibility = '';
      };
    }
  } else {
    let newPlayerCard = createPlayerCard(player);
    animateCard(newPlayerCard, 'in');
    
  }
}


function createPlayerCard(player) {
  const playerCellPosition = document.getElementById("cell-" + player.current_position);
  const newPlayerCard = document.createElement("div");
  newPlayerCard.textContent = player.icon;
  newPlayerCard.className = "player-card";
  newPlayerCard.id = "player-" + player.id;

  playerCellPosition.appendChild(newPlayerCard);
  setNewPLayerCardPostionInCell(playerCellPosition, newPlayerCard);
  return newPlayerCard;
}


function setNewPLayerCardPostionInCell( cell, card ){
    var players  = cell.querySelectorAll('.player-card');
    var players_count = players.length;
    var player_index  = players_count-1;

    var rowIndex    = Math.floor(player_index / 3); 
    var columnIndex = Math.floor(player_index % 3);

    var cellWidth  = cell.clientWidth; // 125
    var cellHeight = cell.clientHeight; // 125

    var cardWidth  = card.clientWidth; // 45
    var cardHeight = card.clientHeight; // 45

    var randomX = (cellWidth / 3 * columnIndex) + ((cellWidth / 3 - cardWidth) / 2);
    var randomY = (cellHeight / 2 * rowIndex) + ((cellHeight / 2 - cardHeight) / 2);

    card.style.left = randomX + 'px';
    card.style.top  = randomY + 'px';

    return { 'randomX': randomX, 'randomY': randomY }
}   


function animateCard(card, animation) {
    // Animation IN: ['fade-in','flip-in','zoom-in','elastic-in','swing-in']
    // Animation OUT: ['slide-out','rotate-out','shrink-out','squeeze-out','drop-out']

    if (card) {

        // Delete last animations
        card.classList.forEach(cls => {
            if (cls.endsWith('-in') || cls.endsWith('-out')) {
            card.classList.remove(cls);
            }
        });

        // Add new
        switch(animation){
            case"in":
                var animation_list = ['fade-in','flip-in','zoom-in','elastic-in','swing-in'];
                var animationClass = getRandomItem(animation_list);
                card.classList.add(animationClass);

                // Delete animation after finish
                card.addEventListener('animationend', function() {
                    card.classList.remove(animationClass);
                  }, { once: true });
                break;

            case"out":
                var animation_list = ['slide-out','rotate-out','shrink-out','squeeze-out','drop-out'];
                var animationClass = getRandomItem(animation_list);
                card.classList.add(animationClass);

                // Delete animation and card after finish
                card.addEventListener('animationend', function() {
                    card.classList.remove(animationClass);
                  }, { once: true });
                break;
        }
    }
}


function getRandomItem(arr) {

    // get random index value
    var randomIndex = Math.floor(Math.random() * arr.length);

    // get random item
    var item = arr[randomIndex];

    return item;
}


async function rollTheDice( diceOne, diceTwo ) {
  rollTheDiceGame.hidden = false;

  let xOne = Math.floor(Math.random() * 6 + 1);
  let xTwo = Math.floor(Math.random() * 6 + 1);

  while (xOne === diceOne) {
    xOne = Math.floor(Math.random() * 6 + 1);
  }
  while (xTwo === diceTwo) {
    xTwo = Math.floor(Math.random() * 6 + 1);
  }

  elDiceOne.className = 'dice show-' + xOne;
  elDiceTwo.className = 'dice show-' + xTwo;

  // Ждём 1 секунду перед броском кубиков
  await new Promise(resolve => setTimeout(resolve, 500));


  for (var i = 1; i <= 6; i++) {
    elDiceOne.classList.remove('show-' + i);
    if (diceOne === i) {
      elDiceOne.classList.add('show-' + i);
    }
  }

  for (var k = 1; k <= 6; k++) {
    elDiceTwo.classList.remove('show-' + k);
    if (diceTwo === k) {
      elDiceTwo.classList.add('show-' + k);
    }
  } 

  // Ждём 2 секунды перед завершением броска
  await new Promise(resolve => setTimeout(resolve, 2000));
  rollTheDiceGame.hidden = true;

}
