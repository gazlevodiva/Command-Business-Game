const voteForButton = document.getElementById("vote_for_btn");
voteForButton?.addEventListener("click", async function () {
  showTurnPreloader(true);
  newVote("VOTE_FOR");
});

const voteAgnButton = document.getElementById("vote_agn_btn");
voteAgnButton?.addEventListener("click", async function () {
  showTurnPreloader(true);
  newVote("VOTE_AGN");
});

const votionModalButton = document.getElementById("votion_btn");
const votionModalBody = document.getElementById("votion_modal_body");

votionModalButton?.addEventListener("click", async function () {
  showTurnPreloader(true);
});

async function newVote(vote_category) {
  try {
    const response = await fetch(
      `/new_vote/${voteMoveIdGlobal}/${playerIdGlobal}/${vote_category}/`
    );
    const data = await response.json();
    return;
  } catch (error) {
    console.error("Ошибка при голосовании:", error);
  }
}

const votion_modal = document.getElementById("votionModal");

function showVotionModal(votion) {
  updateVotionModal(votion);

  var votionModalInstance = new bootstrap.Modal(votion_modal);
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
  }, 2000);
}

function stopVotingStatusCheck() {
  clearInterval(votionInterval);
}

function showVoteModal() {
  const voteModal = document.getElementById("voteModal");
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
  const vote = votes.find((v) => v.player_id === parseInt(playerIdGlobal));
  return vote ? vote.category : false;
}
