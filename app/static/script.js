let timeLeft = 60;
let time_id;
let currentQuestion = 0;
let score = 0;
let userAnswers = [];

function displayQuestion() {
    const currentQuestionData = quizData[currentQuestion];
    const questionCountElement = document.getElementById('questionCount');
    // questionCountElement.textContent = ` ${currentQuestion + 1} / ${quizData.length}`;
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
        const userAnswer = selectedOption.value;
        userAnswers[currentQuestion] = {
            question: quizData[currentQuestion].question_text,
            answer: userAnswer
        };

    }

    else {
      userAnswers[currentQuestion] = {
          question: quizData[currentQuestion].question_text,
          answer: null
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
  if (currentQuestion < quizData.length - 1 && userAnswers[currentQuestion].answer !== null) {
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
    for (let i = 0; i < quizData.length; i++) {
    if (userAnswers[i] === undefined || userAnswers[i].answer === null) {
      userAnswers[i] = {
        question: quizData[i].question_text,
        answer: null
      };
    }
  }
    const queryParams = new URLSearchParams({ score, total, userAnswers: JSON.stringify(userAnswers) }); 
    window.location.href = `/quiz/${quizId}/result?${queryParams.toString()}`;
}

document.getElementById('next').addEventListener('click', nextQuestion);
document.getElementById('prev').addEventListener('click', prevQuestion);
document.getElementById('submit').addEventListener('click', () => {
  const selectedOption = document.querySelector('input[name="quiz"]:checked');
  if (!selectedOption) {
      return;
  }
    checkAnswer();
    redirectToResult();
});

document.querySelectorAll('input[name="quiz"]').forEach(input => {
    input.addEventListener('change', () => {
        document.getElementById('next').disabled = false;
    });
});
displayQuestion();


time_id = setInterval(updateTimer, 1000);
function updateTimer() {
  const totalTime  = 60;
  const circumference = 2 * Math.PI *45;
  const offset = circumference * (timeLeft / totalTime);
  document.querySelector('.inner-circle').style.strokeDashoffset = offset;
  document.getElementById('question-count').innerHTML = `${currentQuestion + 1} / ${quizData.length}`;

    if (timeLeft === 0) {
        clearInterval(time_id);
        setTimeout(function() {
            redirectToResult();
        }, 2000);
    } else {
        timeLeft--;
    }
}

updateTimer();

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
  var passwordInput = document.getElementById("password");
  var passwordIcon = document.getElementById("password-icon");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    passwordIcon.classList.remove("fa-eye");
    passwordIcon.classList.add("fa-eye-slash");
  } else {
    passwordInput.type = "password";
    passwordIcon.classList.remove("fa-eye-slash");
    passwordIcon.classList.add("fa-eye");
  }
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