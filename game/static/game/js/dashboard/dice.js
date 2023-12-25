const rollTheDiceGame = document.getElementById("rollthedice");

const elDiceOne = document.getElementById("dice1");
const elDiceTwo = document.getElementById("dice2");

async function rollTheDice(diceOne, diceTwo) {

  rollTheDiceGame.hidden = false;

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

  await new Promise((resolve) => setTimeout(resolve, 1500));
  rollTheDiceGame.hidden = true;
}
