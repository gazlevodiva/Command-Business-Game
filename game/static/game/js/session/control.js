

window.onload = function () {
  updateSessionPlayers();
  setInterval(updateSessionPlayers, 2500);
};

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

async function updateSessionPlayers() {
  try {
    const response = await fetch("/session_players/");
    const data = await response.json();
    const playersContainer = document.getElementById("sessions-players");

    data.players.forEach((player) => {
      const existingPlayerCard = document.getElementById(`player-card-${player.id}`);
      if (existingPlayerCard) {return}

      const playerCard = document.createElement("div");
      playerCard.classList.add("card", "mb-3");

      playerCard.id = `player-card-${player.id}`;
      playerCard.appendChild(createPlayerSessionCard(player));
      playersContainer.appendChild(playerCard);

    });
  } catch (error) {
    console.error("Error fetching players:", error);
  }
}

function createPlayerSessionCard(player){
  const cardBody = document.createElement('div');
  cardBody.classList.add('card-body');

  const flexContainer = document.createElement('div');
  flexContainer.classList.add('d-flex', 'justify-content-between', 'align-items-center');

  // Player Icon
  const textStart = document.createElement('div');
  textStart.classList.add('text-start', 'text-muted', 'mx-3');

  const iconSpan = document.createElement('span');
  iconSpan.classList.add('h2');
  iconSpan.innerHTML = player.icon;
  textStart.appendChild(iconSpan);

  // Player name
  const textCenter = document.createElement('div');
  textCenter.classList.add('text-center');

  const nameSpan = document.createElement('span');
  nameSpan.classList.add('h4');
  nameSpan.textContent = player.name;
  textCenter.appendChild(nameSpan);

  // Delete button
  if(!player.deletable){
    var textEnd = document.createElement('div');
    textEnd.classList.add('text-end');

    const deleteButton = document.createElement('button');
    deleteButton.type = 'button';
    deleteButton.classList.add('btn', 'text-danger', 'm-0', 'p-0', 'mx-3', 'delete-player-button');
    deleteButton.setAttribute('data-bs-toggle', 'modal');
    deleteButton.setAttribute('data-bs-target', `#deletePlayerModal-${player.id}`);
    deleteButton.setAttribute('data-player-id', player.id);

    const icon = document.createElement('i');
    icon.classList.add('bi', 'bi-trash-fill');
    deleteButton.appendChild(icon);
    textEnd.appendChild(deleteButton);

    var modal = createPlayerSessionDeleteModal(player);
    
  } else {
    var textEnd = document.createElement('div');
    textEnd.classList.add('mx-4');
    var modal = document.createElement('div');
  }

  flexContainer.appendChild(textStart);
  flexContainer.appendChild(textCenter);
  flexContainer.appendChild(textEnd);

  cardBody.appendChild(flexContainer);
  cardBody.appendChild(modal);

  return cardBody;
}

function createPlayerSessionDeleteModal(player){
  const modal = document.createElement('div');
  modal.classList.add('modal', 'fade');
  modal.id = `deletePlayerModal-${player.id}`;
  modal.tabIndex = -1;
  modal.setAttribute('aria-labelledby', `deletePlayerModalLabel-${player.id}`);
  modal.setAttribute('aria-hidden', 'true');

  const modalDialog = document.createElement('div');
  modalDialog.classList.add('modal-dialog', 'modal-dialog-centered');

  const modalContent = document.createElement('div');
  modalContent.classList.add('modal-content');

  const modalHeader = document.createElement('div');
  modalHeader.classList.add('modal-header');

  const modalTitle = document.createElement('h5');
  modalTitle.classList.add('modal-title', 'fs-5');
  modalTitle.id = `deletePlayerModalLabel-${player.id}`;
  modalTitle.textContent = 'Вы хотите удалить игрока?';

  const closeButton = document.createElement('button');
  closeButton.type = 'button';
  closeButton.classList.add('btn-close');
  closeButton.setAttribute('data-bs-dismiss', 'modal');
  closeButton.setAttribute('aria-label', 'Close');
  modalHeader.appendChild(modalTitle);
  modalHeader.appendChild(closeButton);

  const modalBody = document.createElement('div');
  modalBody.classList.add('modal-body', 'text-start');
  modalBody.textContent = `Игрок ${player.name} и все его действия будут удалены.`;

  const modalFooter = document.createElement('div');
  modalFooter.classList.add('modal-footer');

  const deleteConfirmButton = document.createElement('button');
  deleteConfirmButton.type = 'button';
  deleteConfirmButton.classList.add('btn', 'btn-danger');
  deleteConfirmButton.textContent = 'Удалить!';
  deleteConfirmButton.onclick = function() { deletePlayer(player.id); };
  modalFooter.appendChild(deleteConfirmButton);

  modalContent.appendChild(modalHeader);
  modalContent.appendChild(modalBody);
  modalContent.appendChild(modalFooter);
  modalDialog.appendChild(modalContent);
  modal.appendChild(modalDialog);

  return modal;
}
