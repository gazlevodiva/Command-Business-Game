const voteForButton = document.getElementById("vote_for_btn");
voteForButton?.addEventListener("click", async function () {
  showTurnPreloader(true);
  await setNewVote("VOTE_FOR");
});

const voteAgnButton = document.getElementById("vote_agn_btn");
voteAgnButton?.addEventListener("click", async function () {
  showTurnPreloader(true);
  await setNewVote("VOTE_AGN");
});

const voteModal = document.getElementById("voteModal");
const voteDescriptionName = document.getElementById("vote_description_name");
const voteDescriptionCount = document.getElementById("vote_description_count");

const votionModalButton = document.getElementById("votion_btn");
const votionModalBody = document.getElementById("votion_modal_body");
const votionModal = document.getElementById("votionModal");

votionModalButton?.addEventListener("click", async function () {
  showTurnPreloader(true);
});

async function setNewVote(vote_category) {
  try {
    const response = await fetch(`/new_vote/${voteMoveIdGlobal}/${playerIdGlobal}/${vote_category}/`);
    const data = await response.json();
    
    voteModalOpenGlobal = false; // To close vote modal
    return;
  } catch (error) {
    console.error("Error with set new vote:", error);
  }
}



function showVotionModal(votion) {
  updateVotionModal(votion);
  var votionModalInstance = new bootstrap.Modal(votionModal);
  votionModalInstance.show();
}

function updateVotionModal(votion) {
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
      votionModalBody.innerHTML = `<h3>Поздравляем! Вы администратор бизнеса 🎊</h3>`;
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

async function checkVotingStatusCheck(move_id) {
  try {
    const response = await fetch(`/get_votion_data/${move_id}/`);
    const data = await response.json();

    if (data) {
      updateVotionModal(data.votion);
    }
  } catch (error) {
    console.error("Ошибка получения данных:", error);
  }
}

function startVotingStatusCheck(move_id) {
  stopVotingStatusCheck();

  votionInterval = setInterval(() => {
    checkVotingStatusCheck(move_id);
  }, 1000);
}

function stopVotingStatusCheck() {
  clearInterval(votionInterval);
}

function showVoteModal(votion) {
  updateVoteModal(votion);
  var voteModalInstance = new bootstrap.Modal(voteModal);
  voteModalInstance.show();
}

function updateVoteModal(votion){
  voteDescriptionName.innerHTML = `Игрок <b>${votion.player_name}</b> предлагает купить бизнес <b>${votion.business_name}</b> за`;
  voteDescriptionCount.textContent = formatNumber(votion.business_cost);
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
  const vote = votes.find((v) => v.player_id === parseInt(playerIdGlobal));
  return vote ? vote.category : false;
}
