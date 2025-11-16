// Function for opening and closing cards in html. 
function openCard(card) {
  document.getElementById('overlay').style.display = 'flex';
}

function closeCard(event) {
  // Prevent close if clicking inside the card itself
  if (event.target.classList.contains('card') || event.target.classList.contains('basic') || event.target.classList.contains('details')) {
    return;
  }
  document.getElementById('overlay').style.display = 'none';
}


// event listener to add spinning while game loads - for games.html
document.getElementById("play-btn").addEventListener("click", function () {
      // Show game card, hide play card
      document.getElementById("play-card").style.display = "none";
      document.getElementById("game-card").style.display = "block";

      // Wait for iframe to fully load
      const iframe = document.getElementById("game-frame");
      iframe.onload = function () {
          document.getElementById("spinner").style.display = "none";
          iframe.style.opacity = "1";
      };
  });