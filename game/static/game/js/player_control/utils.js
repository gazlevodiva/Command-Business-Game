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

function validateTextarea(textarea) {
  var text = textarea.value.trim();

  var minLength = 4;
  var maxLength = 1000;

  if (text.length === 0) {
    return {"result": false, "desc": 'Поле не может быть пустым или содержать только пробелы.'}
  }

  if (text.length < minLength) {
    return {"result": false, "desc": `Текст должен содержать минимум ${minLength} символов.`}
  }

  if (text.length > maxLength) {
    return {"result": false, "desc": `Текст не должен превышать ${maxLength} символов.`};
  }

  return {"result": true, "desc": 'Ответ подходит.'};
}

// Добавляем обработчик события для формы на "submit"
document.getElementById('memory_answer_form').addEventListener('submit', function(event) {
  // Проверяем валидность текстового поля

  var textarea = document.getElementById('memoryModalTextarea');
  var textareaInvalid = document.getElementById('memoryModalTextareaInvalid');
 
  var valid = validateTextarea(textarea)

  if (!valid.result) {
    textarea.classList.add('is-invalid');
    textareaInvalid.innerText = valid.desc;
    event.preventDefault();
  } else {
    textarea.classList.remove('is-invalid');
    textareaInvalid.innerText = '';
  }
});
