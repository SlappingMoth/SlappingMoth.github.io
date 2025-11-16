
// function to check if the guess was correct

guess = document.getElementById("guess");
missed = document.getElementById("missed-list");


function validate_guess () {

    if (guess == 10){
        missed += 1;
    }

}

