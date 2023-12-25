async function updatePlayerCardOnGameTable(player) {
  const playerCard = document.getElementById("player-" + player.id);

  if (playerCard) {
    const oldPlayerCardCellNumber = parseInt(
      playerCard.parentElement.id.split("-")[1]
    );

    

    if (oldPlayerCardCellNumber !== player.current_position) {

      const newPlayerCell = document.getElementById(
        "cell-" + player.current_position
      );
      let newPlayerCard = createPlayerCard(player);

      newPlayerCard.style.visibility = "hidden";

      const oldRect = playerCard.getBoundingClientRect();
      const newRect = newPlayerCard.getBoundingClientRect();

      playerCard.animate(
        [
          { transform: "translate(0, 0)" },
          {
            transform: `translate(${newRect.left - oldRect.left}px, ${
              newRect.top - oldRect.top
            }px)`,
          },
        ],
        {
          duration: 1000,
          fill: "forwards",
        }
      ).onfinish = () => {
        playerCard.style.position = "";
        playerCard.style.left = "";
        playerCard.style.top = "";
        playerCard.remove();
        newPlayerCard.style.visibility = "";
      };
    }
  } else {
    let newPlayerCard = createPlayerCard(player);
    animateCard(newPlayerCard, "in");
  }
}

function createPlayerCard(player) {
  const playerCellPosition = document.getElementById(
    "cell-" + player.current_position
  );
  const newPlayerCard = document.createElement("div");
  newPlayerCard.textContent = player.icon;
  newPlayerCard.className = "player-card";
  newPlayerCard.id = "player-" + player.id;

  playerCellPosition.appendChild(newPlayerCard);
  setNewPLayerCardPostionInCell(playerCellPosition, newPlayerCard);
  return newPlayerCard;
}

function setNewPLayerCardPostionInCell(cell, card) {
  var players = cell.querySelectorAll(".player-card");
  var players_count = players.length;
  var player_index = players_count - 1;

  var rowIndex = Math.floor(player_index / 3);
  var columnIndex = Math.floor(player_index % 3);

  var cellWidth = cell.clientWidth; // 125
  var cellHeight = cell.clientHeight; // 125
  var cardWidth = card.clientWidth; // 45
  var cardHeight = card.clientHeight; // 45

  var randomX = (cellWidth / 3) * columnIndex + (cellWidth / 3 - cardWidth) / 2;
  var randomY = (cellHeight / 2) * rowIndex + (cellHeight / 2 - cardHeight) / 2;

  card.style.left = randomX + "px";
  card.style.top = randomY + "px";

  return { randomX: randomX, randomY: randomY };
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
        card.classList.add(animationClass);

        card.addEventListener(
          "animationend",
          function () {
            card.classList.remove(animationClass);
          },
          { once: true }
        );
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
        card.classList.add(animationClass);

        card.addEventListener(
          "animationend",
          function () {
            card.classList.remove(animationClass);
          },
          { once: true }
        );
        break;
    }
  }
}

function getRandomItem(arr) {
  var randomIndex = Math.floor(Math.random() * arr.length);
  return arr[randomIndex];
}
