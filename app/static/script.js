let timeLeft = 60;
let time_id = setInterval(countdown, 1000)

function countdown() {
  if (timeLeft == 0) {
    clearInterval(time_id);
    document.getElementById('timer').textContent = 'Time is up';
    setTimeout(function() {
      document.getElementById("quizForm").submit();
    }, 2000);
  
  } else {
    document.getElementById('timer').textContent = `${timeLeft} Seconds remaining`;
    timeLeft --;
  }

}
countdown();

