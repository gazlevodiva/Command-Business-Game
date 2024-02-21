let memoryIndex = document.querySelectorAll("#memories_list .d-flex").length;
const addMemoryButton = document.getElementById("addMemory");
const memoriesForm = document.getElementById("memoriesForm");
const fileInputMemories = document.getElementById("fileInput");

function createMemoryElement(memoryValue = "") {
  const div = document.createElement("div");
  div.className = "mb-3 mt-3 d-flex";
  div.innerHTML = `
    <input type="text" class="form-control" name="memory-${memoryIndex}" id="memory-${memoryIndex}" maxlength="1000" pattern="\\S(.*\\S)?" style="background-color: rgb(244, 244, 244);" value="${memoryValue}" required>
    <button class="btn btn-outline-danger ms-2 deleteMemory">❌</button>
  `;
  memoryIndex++;
  return div;
}

addMemoryButton?.addEventListener("click", function (e) {
  e.preventDefault();
  const memories_list = document.getElementById("memories_list");
  const form = document.getElementById("memoriesForm");
  const newMemoryElement = createMemoryElement();
  memories_list.appendChild(newMemoryElement);
});

memoriesForm?.addEventListener("click", function (e) {
  if (e.target.classList.contains("deleteMemory")) {
    e.preventDefault();
    const parentDiv = e.target.parentElement;
    parentDiv.remove();
  }
});

fileInputMemories?.addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    const formData = new FormData();
    formData.append("file", file);

    fetch("/upload_memory_file/", {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: formData,
    })
    .then((response) => response.json())
    .then((data) => {

        if (data.error) {
          this.value = "";
          var errorFileModal = new bootstrap.Modal(
            document.getElementById("errorFileModal")
          );
          errorFileModal.show();
        } else {
          const memories_list = document.getElementById("memories_list");
          memories_list.innerHTML = "";
          memoryIndex = 0;
          data.memories.forEach((memory) => {
            const newMemoryElement = createMemoryElement(memory[0]);
            memories_list.appendChild(newMemoryElement);
          });
        }

    })
    .catch((error) => console.error("Ошибка загрузки файла:", error));
  }
});

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function resetGame() {
  try {
    const response = await fetch("/reset_game/");
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error game reset:", error);
  }
}

const resetGameButton = document.getElementById("reset-game");
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
