const resetGameButton = document.getElementById("reset-game");

window.onload = function () {
  updateSessionPlayers();
  setInterval(updateSessionPlayers, 2500);
};

resetGameButton?.addEventListener("click", async function () {
  var reset_data = await resetGame();
  var resetGameModal = bootstrap.Modal.getInstance(
    document.getElementById("resetGameModal")
  );

  if (reset_data.result) {
    location.reload();
  } else {
    alert(reset_data.describe);
    console.log(reset_data.error);
  }
});

async function deletePlayer(playerId) {
  var delete_result = await deletePlayerFetch(playerId);

  if (delete_result.result) {
    var player_card = document.getElementById("player-card-" + playerId);
    var resetGameModal = bootstrap.Modal.getInstance(
      document.getElementById("deletePlayerModal-" + playerId)
    );
    resetGameModal.hide();
    player_card.remove();
  } else {
    alert(delete_result.describe);
  }
}

async function deletePlayerFetch(playerId) {
  try {
    const response = await fetch("/delete_player/" + playerId);
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error delete player:", error);
  }
}

async function resetGame() {
  try {
    const response = await fetch("/reset_game/");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();

    console.log(data);

    return data;
  } catch (error) {
    console.error("Error game reset:", error);
  }
}

async function updateSessionPlayers() {
  try {
    const response = await fetch("/session_players/");
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();

    const playersContainer = document.getElementById("sessions-players");

    data.players.forEach((player) => {
      const existingPlayerCard = document.getElementById(
        `player-card-${player.id}`
      );
      if (existingPlayerCard) {
        return;
      }

      const playerCard = document.createElement("div");
      playerCard.classList.add("card", "mb-3");
      playerCard.id = `player-card-${player.id}`;
      playerCard.innerHTML = `
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div class="text-start text-muted mx-3">
                            <span class="h5">${player.icon}</span>
                        </div>
                        <div class="text-center">
                            <span class="h5">${player.name}</span>
                        </div>
                        <div class="text-end">
                            <button 
                                type="button" 
                                class="btn text-danger m-0 p-0 mx-3 delete-player-button"
                                data-bs-toggle="modal" 
                                data-bs-target="#deletePlayerModal-${player.id}"
                                data-player-id="${player.id}"
                            >
                                <i class="bi bi-trash-fill"></i> 
                            </button>
                            <div class="modal fade" id="deletePlayerModal-${player.id}" tabindex="-1" aria-labelledby="deletePlayerModal-${player.id}" aria-hidden="true">
                              <div class="modal-dialog modal-dialog-centered">
                                <div class="modal-content">
                                  <div class="modal-header">
                                    <h1 class="modal-title fs-5" id="deletePlayerModal-${player.id}">Вы хотите удалить игрока?</h1>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                  </div>
                                  <div class="modal-body text-start">
                                    Игрок ${player.name} и все его действия будут удалены. 
                                  </div>
                                  <div class="modal-footer">
                                    <button type="button" class="btn btn-danger" onclick="deletePlayer(${player.id})">Удалить!</button>
                                  </div>
                                </div>
                              </div>
                            </div>
                        </div>
                    </div>
                </div>`;

      playersContainer.appendChild(playerCard);
    });
  } catch (error) {
    console.error("Error fetching players:", error);
  }
}
