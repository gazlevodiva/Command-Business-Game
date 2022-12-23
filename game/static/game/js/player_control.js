
function Preloader(){
  document.getElementById("preloader").hidden = false;
}

const playerBalance = document.getElementById("player_balance");
const investAllCheckbox = document.getElementById("invest_all");
const isCommandCheckbox = document.getElementById("is_command");
const commandInvestInput = document.getElementById("command_invest");
const playerBusinessSelect = document.getElementById("player_business_select");
const commandBusinessSelect = document.getElementById("command_business_select");

investAllCheckbox.addEventListener("change", function() {
  commandInvestInput.value = this.checked ? playerBalance.value : "";
});

isCommandCheckbox.addEventListener("change", function(){
  playerBusinessSelect.hidden = this.checked ? true : false;
  commandBusinessSelect.hidden = this.checked ? false : true;
  playerBusinessSelect.disabled = this.checked;
  commandBusinessSelect.disabled = !this.checked;
});
