const elDiceOne = document.getElementById("dice1");
const elDiceTwo = document.getElementById("dice2");
const game = document.getElementById("rollthedice");

var lastDiceOne = 1;
var lastDiceTwo = 1;

async function rollTheDice() {
  game.hidden = false;

  const diceOne = Math.floor(Math.random() * 6 + 1);
  const diceTwo = Math.floor(Math.random() * 6 + 1);

  let xOne = Math.floor(Math.random() * 6 + 1);
  let xTwo = Math.floor(Math.random() * 6 + 1);

  while (xOne === diceOne) {
    xOne = Math.floor(Math.random() * 6 + 1);
  }
  while (xTwo === diceTwo) {
    xTwo = Math.floor(Math.random() * 6 + 1);
  }

  elDiceOne.className = "dice show-" + xOne;
  elDiceTwo.className = "dice show-" + xTwo;

  // Ждём 1 секунду перед броском кубиков
  await new Promise((resolve) => setTimeout(resolve, 500));

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

  // await MakeAMove(lastDiceOne + lastDiceTwo);
  await MakeAMove(`${lastDiceOne}-${lastDiceTwo}`);
}
