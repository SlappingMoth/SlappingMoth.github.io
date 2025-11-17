
// event listener to add spinning while game loads - for games.html
document.getElementById("play-btn").addEventListener("click", function () {
      // Show game card, hide play card
    document.getElementById("play-card").style.display = "none";
    document.getElementById("game-card").style.display = "block";     
});

document.getElementById("end-btn").addEventListener("click", function () {
    
    // hide game card, show play card
    document.getElementById("play-card").style.display = "block";
    document.getElementById("game-card").style.display = "none";     
});



