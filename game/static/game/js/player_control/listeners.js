// Command Invest Form
const investAllCheckbox = document.getElementById("invest_all");
const commandInvestInput = document.getElementById("command_invest");

const investAllCheckbox2 = document.getElementById("invest_all2");
const commandInvestInput2 = document.getElementById("command_invest2");

investAllCheckbox?.addEventListener("click", function () {
  commandInvestInput.value = playerBalanceGlobal;
});

investAllCheckbox2?.addEventListener("click", function () {
  commandInvestInput2.max = playerBalanceGlobal;
  commandInvestInput2.value = playerBalanceGlobal;
});
