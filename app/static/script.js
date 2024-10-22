let timeLeft = 60;
let time_id;
let currentQuestion = 0;
let score = 0;
let userAnswers = [];

function displayQuestion() {
    const currentQuestionData = quizData[currentQuestion];
    const questionCountElement = document.getElementById('questionCount');
    questionCountElement.textContent = `Question ${currentQuestion + 1} / ${quizData.length}`;
    const questionElement = document.createElement('div');
    questionElement.className = 'question';
    questionElement.textContent = `Question ${currentQuestion + 1}: ${currentQuestionData.question_text}`;

    const optionsElement = document.createElement('div');
    optionsElement.className = 'options';

    currentQuestionData.options.split(',').forEach(option => {
        const label = document.createElement('label');
        label.className = 'option';

        const radio = document.createElement('input');
        radio.type = 'radio';
        radio.name = 'quiz';
        radio.value = option;

        if (userAnswers[currentQuestion] && userAnswers[currentQuestion].answer === option) {
            radio.checked = true;
        }

        label.appendChild(radio);
        label.appendChild(document.createTextNode(option));
        optionsElement.appendChild(label);
    });

    const quizContainer = document.getElementById('quiz');
    quizContainer.innerHTML = '';
    quizContainer.appendChild(questionElement);
    quizContainer.appendChild(optionsElement);

    document.getElementById('prev').disabled = currentQuestion === 0;
    document.getElementById('next').style.display = currentQuestion === quizData.length - 1 ? 'none' : 'inline-block';
    document.getElementById('submit').style.display =  currentQuestion === quizData.length - 1 ? 'inline-block' : 'none';
}

function checkAnswer() {
    const selectedOption = document.querySelector('input[name="quiz"]:checked');
    if (selectedOption) {
        const userAnswer = selectedOption.value.trim();
        userAnswers[currentQuestion] = {
            question: quizData[currentQuestion].question_text,
            answer: userAnswer
        };

    }
}

function prevQuestion() {
  checkAnswer();
  if (currentQuestion > 0) {
    currentQuestion--;
    displayQuestion();
  } 
}

function nextQuestion() {
  checkAnswer();
  if (currentQuestion < quizData.length - 1) {
    currentQuestion++;
    displayQuestion();
  }
}

function redirectToResult() {

   score = userAnswers.reduce((acc, curr, index) => {
       return acc + (curr.answer === quizData[index].answer ? 1 : 0);
   }, 0);
    const total = quizData.length;
    const quizId = quizData[0].quiz_id;
    const queryParams = new URLSearchParams({ score, total, userAnswers: JSON.stringify(userAnswers) }); 
    window.location.href = `/quiz/${quizId}/result?${queryParams.toString()}`;
}

document.getElementById('next').addEventListener('click', nextQuestion);
document.getElementById('prev').addEventListener('click', prevQuestion);
document.getElementById('submit').addEventListener('click', () => {
    checkAnswer();
    redirectToResult();
});

displayQuestion();

time_id = setInterval(countdown, 1000);

function countdown() {
    if (timeLeft === 0) {
        clearInterval(time_id);
        document.getElementById('timer').textContent = 'Time is up';
        setTimeout(function() {
            redirectToResult();
        }, 2000);
    } else {
        document.getElementById('timer').textContent = `${timeLeft} Seconds remaining`;
        timeLeft--;
    }
}
countdown();

document.getElementById('submit').addEventListener('click', checkAnswer);
displayQuestion();


function  toggleAnswers() {
  const answersDiv = document.getElementById('answers');
  const toggleButton = document.getElementById('toggleAnswersBtn');

  if (answersDiv.style.display === "none") {
    answersDiv.style.display = "block";
    toggleButton.textContent = "Hide Answers";
  } else {
    answersDiv.style.display = "none";
    toggleButton.textContent = "Show Answers";
  }
}


function togglePassword() {
  var passwordField = document.getElementById("password");
  var checkbox = document.getElementById("show-password");
  passwordField.type = checkbox.checked ? "text" : "password";
}

 const avatarImages = document.querySelectorAll('.avatar-img');
 const avatarRadios = document.querySelectorAll('input[name="avatar"]');

 function removeSelectedClass() {
    avatarImages.forEach(img => img.classList.remove('avatar-selected'));
 }

avatarRadios.forEach((radio, index) => {
    radio.addEventListener('change', () => {
        removeSelectedClass();
         avatarImages[index].classList.add('avatar-selected');
    }); 
 });
