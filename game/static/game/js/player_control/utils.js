function formatNumber(number) {
  const formatter = new Intl.NumberFormat("ru-RU");
  return formatter.format(number);
}

function playTurnSound() {
  var audio = new Audio("/static/game/files/turn.wav");
  audio.play();
}

function playVibration() {
  navigator.vibrate(500);
}

function showModal(modal) {
  var modalInstance = new bootstrap.Modal(modal);
  modalInstance.show();
}

function removeModalBackdrop() {
  const backdrop = document.querySelector(".modal-backdrop.fade.show");
  if (backdrop) {
    backdrop.remove();
  }
}
