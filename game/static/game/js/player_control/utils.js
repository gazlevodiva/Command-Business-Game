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

// Функция для проверки валидности текстового поля
function validateTextarea() {
  // Получаем текстовое поле по его ID
  var textarea = document.getElementById('memoryModalTextarea');
  var text = textarea.value.trim(); // Удаляем пробелы с обеих сторон

  // Минимальное и максимальное количество символов
  var minLength = 10; // Пример минимального количества символов
  var maxLength = 1000; // Пример максимального количества символов

  // Проверяем, не пусто ли поле после удаления пробелов
  if (text.length === 0) {
    alert('Поле не может быть пустым или содержать только пробелы.');
    return false;
  }

  // Проверяем минимальное количество символов
  if (text.length < minLength) {
    alert(`Текст должен содержать минимум ${minLength} символов.`);
    return false;
  }

  // Проверяем максимальное количество символов
  if (text.length > maxLength) {
    alert(`Текст не должен превышать ${maxLength} символов.`);
    return false;
  }

  // Если все проверки пройдены успешно
  return true;
}

// Добавляем обработчик события для формы на "submit"
document.querySelector('form').addEventListener('submit', function(event) {
  // Проверяем валидность текстового поля
  if (!validateTextarea()) {
    // Если валидация не пройдена, предотвращаем отправку формы
    event.preventDefault();
  }
});
