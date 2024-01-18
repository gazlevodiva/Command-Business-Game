// Globals
var playerTurnGlobal = false;
var playerIdGlobal = "";
var playerNameGlobal = "";
var playerLevelGlobal = 0;
var playerMoveIdGlobal = 0;
var playerBalanceGlobal = 0;
var playerNextCellGlobal = 0;
var playerIsCommandGlobal = false;
var playerCommandShareCount = 0;
var playerCommandShareGlobal = 0;
var voteMoveIdGlobal = 0;

// PLayers details
const playerId = document.getElementById("player_id");
const playerLevel = document.getElementById("player_level");
const playerBalance = document.getElementById("player_balance");
const playerCommandShare = document.getElementById("player_command_share");

// Turn preloader
const playerTurnPreloader = document.getElementById("player_move_preloader");
const playerTurnPreloaderText = document.getElementById(
  "player_move_preloader_text"
);

// Modals
const new_level_modal = document.getElementById("newLevelModal");
const surprise_modal = document.getElementById("surpriseModal");
const memory_modal = document.getElementById("memoryModal");
const command_surprise_modal = document.getElementById("cmndsurpiseModal");
const first_invest_modal = document.getElementById("firstInvestModal");
const skip_move_modal = document.getElementById("skipMoveModal");
const start_modal = document.getElementById("StartModal");
const go_to_start_modal = document.getElementById("goToStartModal");
const random_move_modal = document.getElementById("randomMoveModal");
const back_to_start_modal = document.getElementById("backToStartModal");
const business_btn = document.getElementById("buy-business-modal-button");
const commandBusinessButton = document.getElementById(
  "command_business_button"
);

// Close buttons
const player_move_preloader = document.getElementById("player_move_preloader");
player_move_preloader?.addEventListener("click", whoisTurnPreloader);

const first_invest_cls_btn = document.getElementById("first_invest_close");
first_invest_cls_btn?.addEventListener("click", handleCloseButtonClick);

const business_close_btn_1 = document.getElementById("cls_bsns_btn_1");
business_close_btn_1?.addEventListener("click", handleCloseButtonClick);

const business_close_btn_2 = document.getElementById("cls_bsns_btn_2");
business_close_btn_2?.addEventListener("click", handleCloseButtonClick);

const skip_move_modal_btn = document.getElementById("skipmove_accept");
skip_move_modal_btn?.addEventListener("click", handleCloseButtonClick);

const surprise_close_btn = document.getElementById("surprise_close_btn");
surprise_close_btn?.addEventListener("click", handleCloseButtonClick);

const cmndsurp_close_btn = document.getElementById("cmndsurp_accept");
cmndsurp_close_btn?.addEventListener("click", handleCloseButtonClick);

const success_business_buy_btn = document.getElementById(
  "success-business-buy-btn"
);
success_business_buy_btn?.addEventListener("click", function () {
  showTurnPreloader(true);
});

const start_accept_btn = document.getElementById("start_accept");
start_accept_btn?.addEventListener("click", function () {
  showModal(new_level_modal);
});

const new_level_accept_btn = document.getElementById("new_level_accept");
new_level_accept_btn?.addEventListener("click", async function () {
  if (playerNextCellGlobal) {

    await finishTheMove();
    await MakeAMove(playerNextCellGlobal);

  } else {
    await handleCloseButtonClick();
  }
  playerNextCellGlobal = false;
});

const gotostart_accept_btn = document.getElementById("gotostart_accept");
gotostart_accept_btn?.addEventListener("click", async function () {
  await goToStart();
});

const backtostart_accept_btn = document.getElementById("backtostart_accept");
backtostart_accept_btn?.addEventListener("click", async function () {
  showTurnPreloader(true);
  await backToStart();
});

const randommove_accept_btn = document.getElementById("randommove_accept");
randommove_accept_btn?.addEventListener("click", rollTheDice);

const selector_business_category = document.getElementById(
  "player_business_select_category"
);
selector_business_category?.addEventListener("change", async function () {
  getPlayerBusinessData(selector_business_category.value);
});


const investAllCheckbox = document.getElementById("invest_all");
const commandInvestInput = document.getElementById("command_invest");

const investAllCheckbox2 = document.getElementById("invest_all2");
const commandInvestInput2 = document.getElementById("command_invest2");

investAllCheckbox?.addEventListener("click", function () {
  commandInvestInput.value = playerBalanceGlobal;
});

investAllCheckbox2?.addEventListener("click", function () {
  commandInvestInput2.value = playerBalanceGlobal;
});



window.onload = function () {
  business_btn.hidden = true;

  updatePlayerControlData();
  whoisTurnPreloader();

  // Check is it the player's turn?
  setInterval(() => {
    if (!playerTurnGlobal) {
      whoisTurnPreloader();
    }
  }, 1500);
};


async function handleCloseButtonClick() {
  showTurnPreloader(true);
  await finishTheMove();
}


function showTurnPreloader(show) {
  // // Old version preloader
  // playerTurnPreloaderText.innerText = `Ваш ход окончен.`;
  // playerTurnPreloader.hidden = !show;

  // New version
  document.querySelectorAll('.action-button').forEach(button => {
    if(show){
      playerTurnGlobal = false;
      button.classList.add('disabled');
      button.setAttribute('disabled', 'disabled');
    }
    if(!show){
      
      button.classList.remove('disabled');
      button.removeAttribute('disabled');
    }
  });
}

async function getPlayerControlData(){
  try {
    const response = await fetch(`/get_player_control_data_${playerId.innerHTML}/`);
    const data = await response.json();
    return data;

  } catch (error) {
    console.error("getPlayerControlData error:", error);
  }
}


async function updatePlayerControlData() {
    const data = await getPlayerControlData();

    // Update globals
    playerIdGlobal = data.player_id;
    playerNameGlobal = data.player_name;

    commandInvestInput.max = data.player_balance;
    commandInvestInput2.max = data.player_balance;

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
      playerCommandShare.textContent = 
      `${playerCommandShareGlobal}% (${formatNumber(playerCommandCountGlobal)}) в КБ`;
    }

    if (data.is_open_command_business) {
      playerIsCommandGlobal = data.is_open_command_business;
      commandBusinessButton.hidden = false;
    }


}


async function getWhoisTurn() {
  try {
    const response = await fetch(`/whoisturn/${playerId.innerHTML}/`);
    const data = await response.json();
    return data;

  } catch (error) {
    console.error("Whoisturn error:", error);
  }
}


let voteModalOpenGlobal = false;
async function whoisTurnPreloader() {

  // Get data about players turn
  var data = await getWhoisTurn();
  var is_the_same_player = parseInt(playerId.innerHTML) === parseInt(data.player_id);
  
  playerTurnGlobal = is_the_same_player;

  // Update player info
  await updatePlayerControlData();

  // If this player turn
  if (is_the_same_player) {

      // Hide Turn preloader
      showTurnPreloader(false);

      // Delete BUG with fade
      removeModalBackdrop();

      // Check info about players move
      await whatIsMoveDetails();

      // Make sound and vibro
      playTurnSound();
      playVibration();

  } else {

    // Check votion 
    if(data.votion) {
      if(data.votion.business_status == "VOTING"){
        voteMoveIdGlobal = data.votion.move_id;

        if (hasPlayerVoted(data.votion.votes) === false && !voteModalOpenGlobal) {
          showTurnPreloader(false);
          showVoteModal(data.votion);
          voteModalOpenGlobal = true;
          return;
        }

      }
    }

    showTurnPreloader(true);
    // old version
    // playerTurnPreloader.hidden = is_the_same_player;
    // playerTurnPreloaderText.innerText = `Ход игрока ${data.player_name}.`;
  }
}


async function whatIsMoveDetails() {
  try {
    const response = await fetch(`/move_details_${playerId.innerHTML}/`);
    const data = await response.json();

    const isActionable =
      data.move_stage !== "END" &&
      data.action_category !== "SELL_BIS" &&
      data.action_category !== "CMND";

    if (isActionable) {
      moveReaction(data);
    }
  } catch (error) {
    console.error("Move details error:", error);
  }
}

async function finishTheMove() {
  try {
    const response = await fetch(`/finish_move_${playerMoveIdGlobal}/`);
    const data = await response.json();
    return;
  } catch (error) {
    console.error("Ошибка при завершении хода:", error);
  }
}

async function backToStart() {
  try {
    const response = await fetch(`/back_to_start_${playerMoveIdGlobal}/`);
    const data = await response.json();
    playerMoveIdGlobal = data.move_id;
  } catch (error) {
    console.error("Ошибка при возвращении на старт:", error);
  }
}

async function goToStart() {
  try {
    const response = await fetch(`/go_to_start_${playerMoveIdGlobal}/`);
    const data = await response.json();

    if (data.result) {
      playerMoveIdGlobal = data.move_id;
      await finishTheMove();
      await MakeAMove(11);
    }
  } catch (error) {
    console.error("Ошибка при возвращении на старт:", error);
  }
}

async function moveReaction(data) {
  await updatePlayerControlData();

  var cell_name = data.cell_name;
  playerMoveIdGlobal = data.move_id;

  if (data.next_cell) {
    playerNextCellGlobal = data.next_cell_move;
  }

  if (data.votion) {
    voteMoveIdGlobal = data.votion.move_id;
    if (playerIdGlobal === data.votion.player_id) {
      showVotionModal(data.votion);
      return;
    }
  }

  switch (cell_name) {
    case "start-cell":
      showModal(start_modal);

      await updatePlayerControlData();

      var income = data.is_new_level.income;
      var actions = data.is_new_level.actions;

      var nlwl_income_modal = document.getElementById("new_level_income");
      var nlwl_actions_modal = document.getElementById("new_level_actions");

      nlwl_actions_modal.innerHTML = "";
      nlwl_income_modal.textContent = "💵 Доход круга " + formatNumber(income) + " 💰";

      if (income < 0) {
        nlwl_income_modal.classList.add("text-danger");
      }

      if (actions) {
        actions.forEach(function (action) {
          var paragraph = document.createElement("div");
          paragraph.classList.add("m-2");

          var actionName = document.createElement("span");
          actionName.textContent = action.name + " ";
          paragraph.appendChild(actionName);

          var actionCount = document.createElement("span");
          if (action.count !== 0) {
            actionCount.textContent = formatNumber(action.count);
            if (action.count < 0) {
              actionCount.classList.add("text-danger");
            }
          }

          paragraph.appendChild(actionCount);

          nlwl_actions_modal.appendChild(paragraph);
        });
      }
      break;

    case "go-to-start-cell":
      showModal(go_to_start_modal);
      break;

    case "back-to-start-cell":
      showModal(back_to_start_modal);
      break;

    case "horeca-business-cell":
      showBusinessModal("HORECA");
      break;

    case "realty-business-cell":
      showBusinessModal("REALTY");
      break;

    case "all-business-cell":
      showBusinessModal("ALL");
      break;

    case "science-business-cell":
      showBusinessModal("SCIENCE");
      break;

    case "it-business-cell":
      showBusinessModal("IT");
      break;

    case "memory-cell":
      var memory_name = document.getElementById("memory_name_modal");
      var memory_id_modal = document.getElementsByName("memory_id")[0];
      var move_id_modal = document.getElementsByName("move_id")[0];

      memory_name.textContent = data.action_name;
      memory_id_modal.value = data.memory_id;
      move_id_modal.value = data.move_id;

      showModal(memory_modal);
      break;

    case "surprise-cell":
      var surprise_name = document.getElementById("surprise_name_modal");
      var surprise_count = document.getElementById("surprise_count_modal");

      surprise_name.textContent = data.action_name;
      surprise_count.textContent = formatNumber(data.action_count);

      if (data.action_count < 0) {
        surprise_count.classList.remove("text-success");
        surprise_count.classList.add("text-danger");
        surprise_close_btn.textContent = "Понятно";
      } else {
        surprise_count.classList.remove("text-danger");
        surprise_count.classList.add("text-success");
        surprise_close_btn.textContent = "Спасибо";
      }

      showModal(surprise_modal);
      break;

    case "command-surprise-cell":
      if (data.first_invest_chance) {
        showModal(first_invest_modal);
        break;
      }

      var surprise_name = document.getElementById("cmndsurprise_name_modal");
      var surprise_count = document.getElementById("cmndsurprise_count_modal");

      surprise_name.textContent = data.action_name;
      surprise_count.textContent = formatNumber(data.action_count);

      if (data.action_count < 0) {
        surprise_count.classList.remove("text-success");
        surprise_count.classList.add("text-danger");
      } else {
        surprise_count.classList.remove("text-danger");
        surprise_count.classList.add("text-success");
      }

      showModal(command_surprise_modal);
      break;

    case "random-move-cell":
      showModal(random_move_modal);
      break;

    case "skip-move-cell":
      showModal(skip_move_modal);
      break;
  }
}

async function MakeAMove(diceValue) {
  try {
    const response = await fetch(`/player_move_${playerIdGlobal}_${diceValue}/`);
    const data = await response.json();

    if (data) {
      moveReaction(data);
    }
  } catch (error) {
    console.error("Ошибка при запросе хода:", error);
  }
}

const successBusinessBuyModal = document.getElementById(
  "successBusinessBuyModal"
);

async function buyPersonalBusiness(business_id) {
  try {
    const response = await fetch(
      `/buy_personal_business_${playerIdGlobal}_${business_id}/`
    );
    const data = await response.json();

    if (data.result) {
      showModal(successBusinessBuyModal);
      return;
    }
  } catch (error) {
    console.error("Ошибка при покупке личного бизнеса:", error);
  }
}

async function buyCommandBusiness(business_id) {
  try {
    const response = await fetch(
      `/buy_command_business_${playerIdGlobal}_${business_id}/`
    );
    const data = await response.json();

    if (data.result) {
      showModal(successBusinessBuyModal);
      return;
    }

    if (data.votion) {
      voteMoveIdGlobal = data.votion.move_id;
      showVotionModal(data.votion);
      return;
    }

    return data;
  } catch (error) {
    console.error("Ошибка при покупке командного бизнеса:", error);
  }
}

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
      `/get_player_control_business_data_${playerIdGlobal}_${category}/`
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
      let business_buy_modal = document.getElementById("business_cards");
      business_buy_modal.innerHTML = `
        <div class="text-center h4 mt-4 mb-4">Вы ничего не можете купить 😓</div>
      `;
      return;
    }

    document.getElementById("business_cards").innerHTML = businessCards;
  } catch (error) {
    console.error("Ошибка при получении данных о бизнесе:", error);
  }
}
