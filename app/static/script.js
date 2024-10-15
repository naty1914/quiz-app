let timeLeft = 15;
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

        label.appendChild(radio);
        label.appendChild(document.createTextNode(option));
        optionsElement.appendChild(label);
    });

    const quizContainer = document.getElementById('quiz');
    quizContainer.innerHTML = '';
    quizContainer.appendChild(questionElement);
    quizContainer.appendChild(optionsElement);
}

function checkAnswer() {
    const selectedOption = document.querySelector('input[name="quiz"]:checked');
    if (selectedOption) {
        const userAnswer = selectedOption.value;
        const correctAnswer = quizData[currentQuestion].answer;

        userAnswers.push({
            question: quizData[currentQuestion].question_text,
            answer: userAnswer
        });

        if (userAnswer === correctAnswer) {
          score++;
        }
        currentQuestion++;
        if (currentQuestion < quizData.length) {
            displayQuestion();
        } else {
            redirectToResult();
        }
    }
}

function redirectToResult() {
   for (let j = currentQuestion; j < quizData.length; j++) {
     userAnswers.push({
       question: quizData[j].question_text,
       answer: null
     });
   }
    const total = quizData.length;
    const quizId = quizData[0].quiz_id;
    const queryParams = new URLSearchParams({ score, total, userAnswers: JSON.stringify(userAnswers) }); 
    window.location.href = `/quiz/${quizId}/result?${queryParams.toString()}`;
}

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
