async function updatePlayerCardOnGameTable(player) {
  let playerCard = document.getElementById("player-" + player.id);

  if (playerCard && !playerCard.classList.contains('animating')) {
    const oldPlayerCardCellNumber = parseInt(playerCard.parentElement.id.split("-")[1]);

    if(player.is_turn){
      playerCard.classList.add('pulse');
      playerCard.style.zIndex = "100001";
    } else{
      playerCard.classList.remove('pulse');
      playerCard.style.zIndex = "100000";
    }
    
    if (oldPlayerCardCellNumber !== player.current_position) {

      playerCard.classList.remove('pulse');


      const newPlayerCell = document.getElementById("cell-" + player.current_position);

      var newPlayerCard = createPlayerCard(player, 'new');
      newPlayerCard.style.visibility = "hidden";
        
      const oldRect = playerCard.getBoundingClientRect();
      const newRect = newPlayerCard.getBoundingClientRect();

      playerCard.classList.add('animating');
      playerCard.classList.add('grow');

      let posX = newRect.left - oldRect.left;
      let posY = newRect.top - oldRect.top;

      playerCard.animate(
        [
          { 
            transform: "scale(1) translate(0, 0)",
            offset: 0
          },
          { 
            transform: "scale(1.5) translate(0, 0)",
            offset: 0.2
          },
          { 
            transform: `scale(1) translate(${posX}px, ${posY}px)`,
            offset: 1
          },
        ],
        {
          duration: 1500,
          fill: "forwards",
        }
      ).onfinish = () => {
        playerCard.remove();
        newPlayerCard.style.visibility = "";
        newPlayerCard.id="player-"+player.id;
      };
    }
  } else if (!playerCard) {
    var newPlayerCard = createPlayerCard(player);

    if(player.is_turn){
      newPlayerCard.style.zIndex = "100001";
      newPlayerCard.classList.add('pulse');

    } else {
      animateCard(newPlayerCard, "in");
    }
  }
}

function createPlayerCard(player, newid='') {
  
  const playerCellPosition = document.getElementById("cell-" + player.current_position);
  const cellPlayers = playerCellPosition.querySelectorAll(".player-card");
  const newPlayerCard = document.createElement("div");
  newPlayerCard.textContent = player.icon;
  newPlayerCard.className = "player-card";
  newPlayerCard.id = "player-"+ player.id+newid;


  var index_posible_list = [0, 1, 2, 3, 4, 5];
  let index_occupied_list = [];
  cellPlayers.forEach((playerCard) => {
    index_occupied_list.push(Number(playerCard.getAttribute('data-index')));
  });
  var player_index = index_posible_list.find(index => !index_occupied_list.includes(index));
  newPlayerCard.setAttribute('data-index', player_index);

  playerCellPosition.appendChild(newPlayerCard);
  setNewPLayerCardPostionInCell(playerCellPosition, newPlayerCard);
  return newPlayerCard;
}

function setNewPLayerCardPostionInCell(cell, card) {
  var player_index = Number(card.getAttribute('data-index'));
  var rowIndex = Math.floor(player_index / 3);
  var columnIndex = player_index % 3;

  var cellWidth = cell.clientWidth;
  var cellHeight = cell.clientHeight;
  var cardWidth = card.clientWidth;
  var cardHeight = card.clientHeight;

  var randomX = (cellWidth / 3) * columnIndex + (cellWidth / 3 - cardWidth) / 2;
  var randomY = (cellHeight / 2) * rowIndex + (cellHeight / 2 - cardHeight) / 2;

  card.style.left = randomX + "px";
  card.style.top = randomY + "px";

  return {randomX: randomX, randomY: randomY, index: player_index};
}

function animateCard(card, animation) {
  // Animation IN: ['fade-in','flip-in','zoom-in','elastic-in','swing-in']
  // Animation OUT: ['slide-out','rotate-out','shrink-out','squeeze-out','drop-out']

  if (card) {
    card.classList.forEach((cls) => {
      if (cls.endsWith("-in") || cls.endsWith("-out")) {
        card.classList.remove(cls); // Delete last animations
      }
    });

    // Add new
    switch (animation) {
      case "in":
        var animation_list = [
          "fade-in",
          "flip-in",
          "zoom-in",
          "elastic-in",
          "swing-in",
        ];
        var animationClass = getRandomItem(animation_list);
        break;

      case "out":
        var animation_list = [
          "slide-out",
          "rotate-out",
          "shrink-out",
          "squeeze-out",
          "drop-out",
        ];
        var animationClass = getRandomItem(animation_list);
        break;
    }

    card.classList.add(animationClass);
    card.addEventListener("animationend",function () {
      card.classList.remove(animationClass);
    },
      { once: true }
    );
  }
}

function getRandomItem(arr) {
  var randomIndex = Math.floor(Math.random() * arr.length);
  return arr[randomIndex];
}
