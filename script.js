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

