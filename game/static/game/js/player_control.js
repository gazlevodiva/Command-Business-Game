// PLayers details
const playerId = document.getElementById("player_id").innerHTML;
const playerLevel = document.getElementById("player_level");
const playerBalance = document.getElementById("player_balance");
const playerCommandShare = document.getElementById("player_command_share");

const playerTurnPreloader = document.getElementById("player_move_preloader");
const playerTurnPreloaderText = document.getElementById(
  "player_move_preloader_text"
);

const investAllCheckbox = document.getElementById("invest_all");
const investAllCheckbox2 = document.getElementById("invest_all2");

const commandInvestInput = document.getElementById("command_invest");
const commandInvestInput2 = document.getElementById("command_invest2");

const playerBusinessSelect = document.getElementById("player_business_select");
const commandBusinessSelect = document.getElementById(
  "command_business_select"
);
const selector_business_category = document.getElementById(
  "player_business_select_category"
);
const commandBusinessButton = document.getElementById(
  "command_business_button"
);

var move_id = 0;

var business_close_btn_1 = document.getElementById("cls_bsns_btn_1");
var business_close_btn_2 = document.getElementById("cls_bsns_btn_2");
var surprise_close_btn = document.getElementById("surprise_close_btn");
var memory_close_btn = document.getElementById("memory_accept_btn");
var cmndsurp_close_btn = document.getElementById("cmndsurp_accept");
var gotostart_accept_btn = document.getElementById("gotostart_accept");
var start_accept_btn = document.getElementById("start_accept");
var new_level_accept_btn = document.getElementById("new_level_accept");
var backtostart_accept_btn = document.getElementById("backtostart_accept");
var randommove_accept = document.getElementById("randommove_accept");

const elDiceOne = document.getElementById("dice1");
const elDiceTwo = document.getElementById("dice2");

const game = document.getElementById("rollthedice");
const business_btn = document.getElementById("buy-business-modal-button");
const business_modal = document.getElementById(
  "BusinessModal" + playerId + "2"
);
const new_level_modal = document.getElementById("newLevelModal");
const surprise_modal = document.getElementById("surpriseModal");
const memory_modal = document.getElementById("memoryModal");

const command_surprise_modal = document.getElementById("cmndsurpiseModal");
const first_invest_modal = document.getElementById("firstInvestModal");
const first_invest_cls_btn = document.getElementById("first_invest_close");

const skip_move_modal = document.getElementById("skipMoveModal");
const skip_move_modal_btn = document.getElementById("skipmove_accept");

const start_modal = document.getElementById("StartModal");
const go_to_start_modal = document.getElementById("goToStartModal");
const random_move_modal = document.getElementById("randomMoveModal");
const back_to_start_modal = document.getElementById("backToStartModal");

const votionModal = document.getElementById("votionModal");
const voteModal = document.getElementById("voteModal");
const votionModalButton = document.getElementById("votion_btn");
const votionModalBody = document.getElementById("votion_modal_body");
const successBusinessBuyModalButton = document.getElementById(
  "successBusinessBuyModal"
);

const voteForBtn = document.getElementById("vote_for_btn");
const voteAgnBtn = document.getElementById("vote_agn_btn");

// IMPORTANT VARIABLES

// PLayers detail
var playerIdGlobal = "";
var playerNameGlobal = "";
var playerBalanceGlobal = 0;
var playerLevelGlobal = 0;

var playerIsCommandGlobal = false;
var playerCommandShareGlobal = 0;
var playerCommandShareCount = 0;

var playerMoveIdGlobal = 0;
var playerNextCellGlobal = 0;

var voteMoveIdGlobal = 0;

// Other
var lastDiceOne = 1;
var lastDiceTwo = 1;

game.hidden = true;
business_btn.hidden = true;

window.addEventListener("load", whoisTurnPreloader);

investAllCheckbox?.addEventListener("click", function () {
  commandInvestInput.value = playerBalanceGlobal;
});

investAllCheckbox2?.addEventListener("click", function () {
  commandInvestInput2.max = playerBalanceGlobal;
  commandInvestInput2.value = playerBalanceGlobal;
});

// When
document
  .getElementById("player_move_preloader")
  .addEventListener("click", whoisTurnPreloader);

successBusinessBuyModalButton?.addEventListener(
  "click",
  handleCloseButtonClick
);
first_invest_cls_btn?.addEventListener("click", handleCloseButtonClick);
business_close_btn_1?.addEventListener("click", handleCloseButtonClick);
business_close_btn_2?.addEventListener("click", handleCloseButtonClick);
skip_move_modal_btn?.addEventListener("click", handleCloseButtonClick);
surprise_close_btn?.addEventListener("click", handleCloseButtonClick);
cmndsurp_close_btn?.addEventListener("click", handleCloseButtonClick);

new_level_accept_btn?.addEventListener("click", async function () {
  if (playerNextCellGlobal) {
    await finishTheMove();
    await AskTheMove(playerNextCellGlobal);
  } else {
    await handleCloseButtonClick();
  }
  playerNextCellGlobal = false;
});

gotostart_accept_btn?.addEventListener("click", async function () {
  await goToStart();
});

backtostart_accept_btn?.addEventListener("click", async function () {
  showTurnPreloader();
  await backToStart();
});

randommove_accept?.addEventListener("click", async function () {
  // Finish random move before start new move
  await finishTheMove();
  rollTheDice();
});

async function handleCloseButtonClick() {
  showTurnPreloader();
  await finishTheMove();
}

function showTurnPreloader() {
  playerTurnPreloaderText.innerText = `Ваш ход окончен.`;
  playerTurnPreloader.hidden = false;
}

function hideTurnPreloader() {
  playerTurnPreloader.hidden = true;
}

async function updatePlayerControlData() {
  try {
    const response = await fetch(`/get_player_control_data_${playerId}/`);
    if (!response.ok) {
      throw new Error("Network response was not ok.");
    }
    const data = await response.json();

    // Update globals
    playerNameGlobal = data.player_name;

    if (playerLevelGlobal != data.player_level) {
      playerLevelGlobal = data.player_level;
      playerLevel.textContent = `${playerLevelGlobal} круг`;
    }

    if (playerBalanceGlobal != data.player_balance) {
      playerBalanceGlobal = data.player_balance;
      playerBalance.textContent = formatNumber(playerBalanceGlobal);
      playerBalance.classList.toggle("text-danger", playerBalanceGlobal < 0);
    }

    if (playerCommandShareGlobal != data.command_share) {
      playerCommandShareGlobal = data.command_share;
      playerCommandCountGlobal = data.command_count;
      playerCommandBankGlobal = data.command_bank;
      playerCommandShare.textContent = `${playerCommandShareGlobal}% (${formatNumber(
        playerCommandCountGlobal
      )}) в КБ`;
    }

    if (data.is_open_command_business) {
      playerIsCommandGlobal = data.is_open_command_business;
      commandBusinessButton.hidden = false;
    }
  } catch (error) {
    console.error("Error updating player control data:", error);
  }
}

async function whoisTurnPreloader() {
  try {
    const response = await fetch("/whoisturn/" + playerId + "/");
    const data = await response.json();

    const { player_id, player_name } = data;

    var same_player = parseInt(playerId) === parseInt(data.player_id);

    // console.log( 'whoisturn', data )

    if (same_player) {
      playerTurnPreloaderText.innerText = `Ваш ход окончен.`;
      hideTurnPreloader();
      await updatePlayerControlData();
      await whatIsMoveDetails();

      // Sound and vibro notification
      playTurnSound();
      playVibration();
    } else {
      if (data.votion) {
        voteMoveIdGlobal = data.votion.move_id;
        if (hasPlayerVoted(data.votion.votes) === false) {
          hideTurnPreloader();
          showVoteModal();
          return;
        }
      }

      await updatePlayerControlData();
      playerTurnPreloader.hidden =
        parseInt(playerId) === parseInt(data.player_id);
      playerTurnPreloaderText.innerText = `Ход игрока ${player_name}.`;
    }
  } catch (error) {
    console.error("Ошибка при определении очереди хода:", error);
  }
}

async function whatIsMoveDetails() {
  try {
    const response = await fetch(`/move_details_${playerId}/`);
    const data = await response.json();

    if (isMoveActionable(data)) {
      moveReaction(data);
    }
  } catch (error) {
    console.error("Ошибка при получении деталей хода:", error);
  }
}

function isMoveActionable(data) {
  return (
    data["move_stage"] !== "END" &&
    data["action_category"] !== "SELL_BIS" &&
    data["action_category"] !== "CMND"
  );
}

async function finishTheMove() {
  try {
    const response = await fetch(`/finish_move_${playerMoveIdGlobal}/`);
    if (!response.ok) {
      throw new Error("Network response was not ok.");
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Ошибка при завершении хода:", error);
  }
}

async function backToStart() {
  try {
    const response = await fetch(`/back_to_start_${playerMoveIdGlobal}/`);
    if (!response.ok) {
      throw new Error("Network response was not ok.");
    }
    const data = await response.json();
    if (data.result) {
      playerMoveIdGlobal = data.move_id;
      return data;
    }
  } catch (error) {
    console.error("Ошибка при возвращении на старт:", error);
  }
}

async function goToStart() {
  try {
    const response = await fetch(`/go_to_start_${playerMoveIdGlobal}/`);
    if (!response.ok) {
      throw new Error("Network response was not ok.");
    }
    const data = await response.json();
    if (data.result) {
      playerMoveIdGlobal = data.move_id;
      // Finish back-to-start mome before start new level move
      finishTheMove();
      AskTheMove(11);
      return data;
    }
  } catch (error) {
    console.error("Ошибка при возвращении на старт:", error);
  }
}

async function buyPersonalBusiness(business_id) {
  try {
    const response = await fetch(
      `/buy_personal_business_${playerId}_${business_id}/`
    );
    if (!response.ok) {
      throw new Error("Network response was not ok.");
    }
    const data = await response.json();
    if (data.result) {
      // showTurnPreloader();
      const successBusinessBuyModal = document.getElementById(
        "successBusinessBuyModal"
      );
      var successBusinessBuyModalInstance = new bootstrap.Modal(
        successBusinessBuyModal
      );
      successBusinessBuyModalInstance.show();
      return data;
    }
  } catch (error) {
    console.error("Ошибка при покупке личного бизнеса:", error);
  }
}

async function buyCommandBusiness(business_id) {
  try {
    const response = await fetch(
      `/buy_command_business_${playerId}_${business_id}/`
    );
    if (!response.ok) {
      throw new Error("Network response was not ok.");
    }
    const data = await response.json();

    console.log("buyCommandBusiness", data);

    if (data.result) {
      // showTurnPreloader();
      const successBusinessBuyModal = document.getElementById(
        "successBusinessBuyModal"
      );
      var successBusinessBuyModalInstance = new bootstrap.Modal(
        successBusinessBuyModal
      );
      successBusinessBuyModalInstance.show();
      return data;
    }

    if (data.votion) {
      voteMoveIdGlobal = data.votion.move_id;
      showVotionModal(data.votion);
      return data;
    }

    return data;
  } catch (error) {
    console.error("Ошибка при покупке командного бизнеса:", error);
  }
}

selector_business_category?.addEventListener("change", function () {
  getPlayerBusinessData(selector_business_category.value);
});

function createBusinessCard(
  business,
  playerBalance,
  commandBank,
  commandShare
) {
  const canBuyPersonal = business.fields.cost <= playerBalance;
  const canBuyCommand = business.fields.cost <= commandBank && commandShare > 0;

  if (canBuyPersonal || canBuyCommand) {
    return `
      <div class="card mb-4">
        <div class="card-body p-4">
          <div class="card-title">
            <div class="row">
              <div class="col">
                <h5 class="card-title mb-0">${business.fields.name}</h5>
              </div>
              <div class="col text-end">
                <h5 class="card-text mb-0">${formatNumber(
                  business.fields.cost
                )}</h5>
              </div>
            </div>
          </div>
          <p class="card-text">Рентабельность: от ${
            business.fields.min_rent
          }% до ${business.fields.max_rent}%</p>
        </div>
        <div class="card-footer">
          <div class="row">
            <div class="col-6 px-1">
              <button class="btn ${
                canBuyPersonal ? "btn-success" : ""
              } w-100" data-bs-dismiss="modal" onclick="buyPersonalBusiness(${
      business.pk
    })" ${!canBuyPersonal ? "disabled" : ""}>
                Личный бизнес
              </button>
            </div>
            <div class="col-6 px-1">
              <button class="btn ${
                canBuyCommand ? "btn-danger" : ""
              } w-100" data-bs-dismiss="modal" onclick="buyCommandBusiness(${
      business.pk
    })" ${!canBuyCommand ? "disabled" : ""}>
                Командный бизнес
              </button>
            </div>
          </div>
        </div>
      </div>
    `;
  } else {
    return;
  }
}

async function getPlayerBusinessData(category) {
  try {
    const response = await fetch(
      `/get_player_control_business_data_${playerId}_${category}/`
    );
    const data = await response.json();

    const businessCards = data.businesses
      .map((business) =>
        createBusinessCard(
          business,
          data.player_balance,
          data.command_bank,
          data.command_share
        )
      )
      .join("");

    // If not businesses to buy
    if (businessCards == "") {
      let business_buy_modal = document.getElementById(
        "buy_business_modal_body"
      );
      business_buy_modal.innerHTML =
        '<div class="text-center h3">Вы ничего не можете купить 😓</div>';
      return;
    }

    document.getElementById("business_cards").innerHTML = businessCards;
  } catch (error) {
    console.error("Ошибка при получении данных о бизнесе:", error);
  }
}

async function moveReaction(data) {
  var move_id = data.move_id;
  var cell_name = data.cell_name;
  playerMoveIdGlobal = move_id;

  if (data.next_cell) {
    playerNextCellGlobal = data.next_cell_move;
  }

  if (data.votion) {
    voteMoveIdGlobal = data.votion.move_id;
    if (parseInt(playerId) === data.votion.player_id) {
      showVotionModal(data.votion);
      return;
    }
  }

  switch (cell_name) {
    case "start-cell":
      var startModalInstance = new bootstrap.Modal(start_modal);
      startModalInstance.show();

      start_accept_btn?.removeEventListener("click", null);
      start_accept_btn?.addEventListener("click", function () {
        var newLevelModalInstance = new bootstrap.Modal(new_level_modal);

        // Here is data for modal
        var income = data["is_new_level"]["income"];
        var actions = data["is_new_level"]["actions"];

        var nlwl_income_modal = document.getElementById("new_level_income");
        var nlwl_actions_modal = document.getElementById("new_level_actions");

        nlwl_income_modal.textContent = "Вы заработали " + income;
        nlwl_actions_modal.innerHTML = "";

        console.log(actions);

        if (typeof actions === "string") {
          var paragraph = document.createElement("div");
          paragraph.textContent = actions;
          nlwl_actions_modal.appendChild(paragraph);
        } else if (Array.isArray(actions)) {
          actions.forEach(function (action) {
            var paragraph = document.createElement("div m-2");

            var actionName = document.createElement("span");
            actionName.textContent = action.name + " ";
            paragraph.appendChild(actionName);

            var actionCount = document.createElement("span");
            actionCount.textContent = action.count;

            if (action.count < 0) {
              actionCount.classList.add("text-danger");
            }

            paragraph.appendChild(actionCount);
            nlwl_actions_modal.appendChild(paragraph);
          });
        }

        newLevelModalInstance.show();
      });
      break;

    case "go-to-start-cell":
      var goToStartModalInstance = new bootstrap.Modal(go_to_start_modal);
      goToStartModalInstance.show();
      break;

    case "back-to-start-cell":
      var backToStartModalInstance = new bootstrap.Modal(back_to_start_modal);
      backToStartModalInstance.show();
      break;

    case "horeca-business-cell":
      var horecaBusinessModalInstance = new bootstrap.Modal(business_modal);
      selector_business_category.value = "HORECA";
      getPlayerBusinessData("HORECA");
      selector_business_category.disabled = true;
      horecaBusinessModalInstance.show();
      break;

    case "realty-business-cell":
      var realtyBusinessModalInstance = new bootstrap.Modal(business_modal);
      selector_business_category.value = "REALTY";
      getPlayerBusinessData("REALTY");
      selector_business_category.disabled = true;
      realtyBusinessModalInstance.show();
      break;

    case "all-business-cell":
      var allBusinessModalInstance = new bootstrap.Modal(business_modal);
      selector_business_category.value = "ALL";
      getPlayerBusinessData("ALL");
      // selector_business_category.disabled = true; #Don`t need in ALL category
      allBusinessModalInstance.show();
      break;

    case "science-business-cell":
      var scienceBusinessModalInstance = new bootstrap.Modal(business_modal);
      selector_business_category.value = "SCIENCE";
      getPlayerBusinessData("SCIENCE");
      selector_business_category.disabled = true;
      scienceBusinessModalInstance.show();
      break;

    case "it-business-cell":
      var itBusinessModalInstance = new bootstrap.Modal(business_modal);
      selector_business_category.value = "IT";
      getPlayerBusinessData("IT");
      selector_business_category.disabled = true;
      itBusinessModalInstance.show();
      break;

    case "memory-cell":
      var memoryModalInstance = new bootstrap.Modal(memory_modal);
      var memory_name = document.getElementById("memory_name_modal");
      var memory_id_modal = document.getElementsByName("memory_id")[0];
      var move_id_modal = document.getElementsByName("move_id")[0];

      memory_name.textContent = data["action_name"];
      memory_id_modal.value = data["memory_id"];
      move_id_modal.value = data["move_id"];

      memoryModalInstance.show();
      break;

    case "surprise-cell":
      var surpriseModal = document.getElementById("surpriseModal");

      var surprise_name = document.getElementById("surprise_name_modal");
      var surprise_count = document.getElementById("surprise_count_modal");

      console.log(data.action_name);

      surprise_name.textContent = data.action_name;
      surprise_count.textContent = data.action_count;

      if (data.action_count < 0) {
        surprise_count.classList.remove("text-success");
        surprise_count.classList.add("text-danger");
        surprise_close_btn.textContent = "Понятно";
      } else {
        surprise_count.classList.remove("text-danger");
        surprise_count.classList.add("text-success");
        surprise_close_btn.textContent = "Спасибо";
      }
      var surpriseModalInstance = new bootstrap.Modal(surpriseModal);
      surpriseModalInstance.show();
      break;

    case "command-surprise-cell":
      var commandSurpriseModalInstance = new bootstrap.Modal(
        command_surprise_modal
      );
      var surprise_name = document.getElementById("cmndsurprise_name_modal");
      var surprise_count = document.getElementById("cmndsurprise_count_modal");

      if (data["first_invest_chance"]) {
        var firstInvestModalInstance = new bootstrap.Modal(first_invest_modal);

        // surprise_name.textContent = "Ваш первый шанс на инвестицию. Будете инвестировать?";

        firstInvestModalInstance.show();
        break;
      } else {
        surprise_name.textContent = data["action_name"];
        surprise_count.textContent = data["action_count"];
        if (data["action_count"] < 0) {
          surprise_count.classList.remove("text-success");
          surprise_count.classList.add("text-danger");
        } else {
          surprise_count.classList.remove("text-danger");
          surprise_count.classList.add("text-success");
        }
      }

      commandSurpriseModalInstance.show();
      break;

    case "random-move-cell":
      var randomMoveModalInstance = new bootstrap.Modal(random_move_modal);
      randomMoveModalInstance.show();
      break;

    case "skip-move-cell":
      var skipMoveModalInstance = new bootstrap.Modal(skip_move_modal);
      skipMoveModalInstance.show();
      break;
  }
}

async function AskTheMove(diceValue) {
  try {
    const response = await fetch(`/player_move_${playerId}_${diceValue}/`);
    const data = await response.json();
    moveReaction(data);
  } catch (error) {
    console.error("Ошибка при запросе хода:", error);
  }
}

async function WhatTheMove(diceValue, callback) {
  await AskTheMove(diceValue);
  setTimeout(callback, 1000);
}

async function rollTheDice() {
  game.hidden = false;

  // Ждём 1 секунду перед броском кубиков
  await new Promise((resolve) => setTimeout(resolve, 500));

  const diceOne = Math.floor(Math.random() * 6 + 1);
  const diceTwo = Math.floor(Math.random() * 6 + 1);

  for (var i = 1; i <= 6; i++) {
    elDiceOne.classList.remove("show-" + i);
    if (diceOne === i) {
      elDiceOne.classList.add("show-" + i);
    }
  }

  for (var k = 1; k <= 6; k++) {
    elDiceTwo.classList.remove("show-" + k);
    if (diceTwo === k) {
      elDiceTwo.classList.add("show-" + k);
    }
  }

  lastDiceOne = diceOne;
  lastDiceTwo = diceTwo;

  // Ждём 2 секунды перед завершением броска
  await new Promise((resolve) => setTimeout(resolve, 2000));
  game.hidden = true;

  await WhatTheMove(lastDiceOne + lastDiceTwo);
}

function formatNumber(number) {
  const formatter = new Intl.NumberFormat("en-US");
  return formatter.format(number);
}

function playTurnSound() {
  var audio = new Audio("/static/game/files/turn.wav");
  audio.play();
}

function playVibration() {
  navigator.vibrate(500);
}

voteForBtn?.addEventListener("click", function () {
  newVote("VOTE_FOR");
});

voteAgnBtn?.addEventListener("click", function () {
  newVote("VOTE_AGN");
});

async function newVote(vote_category) {
  try {
    const response = await fetch(
      `/new_vote/${voteMoveIdGlobal}/${playerId}/${vote_category}/`
    );
    const data = await response.json();

    if (data) {
      showTurnPreloader();
    }
  } catch (error) {
    console.error("Ошибка при голосовании:", error);
  }
}

function showVotionModal(votion) {
  var votionModalInstance = new bootstrap.Modal(votionModal);
  updateVotionModal(votion);
  votionModalInstance.show();
}

function updateVotionModal(votion) {
  console.log("updateVotionModal", votion, votion["votion"]);

  switch (votion.business_status) {
    case "VOTING":
      votionModalBody.innerHTML = `
        <h4> <b>${votion.business_name}</b>. Идет голосование ...</h4>
        <h2>✅ ${votion.votes_for_count} / ${votion.votes_agn_count} ❌</h2>
      `;

      votionModalButton.textContent = "Идет голосование...";
      votionModalButton.disabled = true;

      startVotingStatusCheck(votion.move_id);
      break;

    case "ACTIVE":
      votionModalBody.innerHTML = `<h3>🎉 Вы администратор бизнеса 🎊</h3>`;
      votionModalButton.textContent = "Спасибо";
      votionModalButton.disabled = false;
      stopVotingStatusCheck();
      break;

    case "UNVOTE":
      votionModalBody.innerHTML = `<h4>К сожалению вам не удалось приобрести бизнес 😞</h4>`;
      votionModalButton.textContent = "Понятно";
      votionModalButton.disabled = false;
      stopVotingStatusCheck();
      break;
  }
}

let votionInterval;

function startVotingStatusCheck(move_id) {
  stopVotingStatusCheck();
  votionInterval = setInterval(() => {
    fetch(`/get_votion_data/${move_id}/`)
      .then((response) => response.json())
      .then((data) => {
        updateVotionModal(data.votion);
      })
      .catch((error) => console.error("Ошибка получения данных:", error));
  }, 2000); // Интервал в 2 секунды
}

function stopVotingStatusCheck() {
  clearInterval(votionInterval);
}

function showVoteModal() {
  var voteModalInstance = new bootstrap.Modal(voteModal);
  voteModalInstance.show();
}

function countVotes(votes) {
  let voteCounts = { VOTE_FOR: 0, VOTE_AGN: 0 };
  votes.forEach((vote) => {
    if (vote.category === "VOTE_FOR") {
      voteCounts.VOTE_FOR += 1;
    } else if (vote.category === "VOTE_AGN") {
      voteCounts.VOTE_AGN += 1;
    }
  });
  return voteCounts;
}

function hasPlayerVoted(votes) {
  const vote = votes.find((v) => v.player_id === parseInt(playerId));
  return vote ? vote.category : false;
}
