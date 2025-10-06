// script.js
let player1Score = 0;
let player2Score = 0;
let isTwoPlayerMode = false;
let player1Turn = true;
let player1Choice = '';
let player2Choice = '';

const modeSelect = document.getElementById('mode-select');
const player1ScoreSpan = document.getElementById('player1-score');
const player2ScoreSpan = document.getElementById('player2-score');
const resultDiv = document.getElementById('result');
const choicesButtons = document.querySelectorAll('.choice');

// event listener - pretty simple
modeSelect.addEventListener('change', function() {
    isTwoPlayerMode = this.value === 'multi';
    resetGame();
});

// given the amount of players, play the game
choicesButtons.forEach(button => {
    button.addEventListener('click', function() {
        if (!isTwoPlayerMode) {
            // Single player mode
            playRound(this.id, getComputerChoice());
        } else {
            // Two player mode logic
            if (player1Turn) {
                player1Choice = this.id;
                player1Turn = false;
                resultDiv.innerText = 'Player 2: Make your choice';
            } else {
                player2Choice = this.id;
                playRound(player1Choice, player2Choice);
                player1Turn = true; // Reset for next round
            }
        }
    });
});

document.getElementById('reset').addEventListener('click', resetGame);

// given 1 player have the computer make a choice
function getComputerChoice() {
    const choices = ['rock', 'paper', 'scissors'];
    return choices[Math.floor(Math.random() * 3)];
}

// play a round of rock-paper-scissors
function playRound(player1Choice, player2Choice) {
    const winner = getWinner(player1Choice, player2Choice);
    updateScore(winner);
    displayResult(player1Choice, player2Choice, winner);
}

// given the choices of uesers, calcculate the winner
function getWinner(player1Choice, player2Choice) {
    if (player1Choice === player2Choice) {
        return 'draw';
    }
    // logic to calculate the winner
    if ((player1Choice === 'rock' && player2Choice === 'scissors') ||
        (player1Choice === 'scissors' && player2Choice === 'paper') ||
        (player1Choice === 'paper' && player2Choice === 'rock')) {
        return 'player1';
    }
    
    return 'player2';
}

// update the score based on the result of the game
function updateScore(winner) {
    if (winner === 'player1') {
        player1Score++;
        player1ScoreSpan.innerText = player1Score;
    } else if (winner === 'player2') {
        player2Score++;
        player2ScoreSpan.innerText = player2Score;
    }
    // No score update for a draw
}

// display the players choice and result to the user
function displayResult(player1Choice, player2Choice, winner) {
    let resultMessage;
    if (winner === 'draw') {
        resultMessage = `Both chose ${player1Choice}. It's a draw!`;
    } else {
        let winnerText = winner === 'player1' ? 'Player 1' : 'Player 2';
        resultMessage = `Player 1 chose ${player1Choice}. Player 2 chose ${player2Choice}. ${winnerText} wins!`;
    }
    resultDiv.innerText = resultMessage;
}

// reset the game start back to beginning state
function resetGame() {
    player1Score = 0;
    player2Score = 0;
    player1Turn = true;
    player1Choice = '';
    player2Choice = '';
    player1ScoreSpan.innerText = player1Score;
    player2ScoreSpan.innerText = player2Score;
    resultDiv.innerText = '';
}