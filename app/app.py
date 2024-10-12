from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import  Question, Quiz, QuizResult, User


app = Blueprint('app', __name__)

@app.route('/')
def index():
    """It renders the index.html template."""
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """It renders the registration.html template."""
    if request.method == 'POST':
        username = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Username: {username}, Email: {email}, Password: {password}")
        
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('registration.html', error='Email  already exists. Please try again.')
        existing_username = User.query.filter_by(username=username).first()
        if existing_username:
           error_message = 'Username already exists. Please try again.'
           return render_template('registration.html', error=error_message) 
        
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('app.login'))

    return render_template('registration.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    """It renders the login.html template."""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
      
        if user and user.check_password(password):
            login_user(user)
            print("login successful")
            return redirect(url_for('app.dashboard'))
        else:
            return render_template('login.html', error='Login failed. Please check your email and password.')
    
    return render_template('login.html')  


@app.route('/dashboard')
@login_required 
def dashboard():
    """It renders the dashboard.html template."""
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
def logout():
    """It logs out the user."""
    print("logging out")
    logout_user()
    return redirect(url_for('app.index'))


@app.route('/quiz_categories')
@login_required
def quizzes():
    """It renders the quiz_categories.html template."""
    quizzes = Quiz.query.all()
    return render_template('quiz_categories.html', quizzes=quizzes)

@app.route('/quiz/<int:quiz_id>')
@login_required
def quiz(quiz_id):
    """It renders the quiz.html template."""
    quiz = Quiz.query.get(quiz_id) 
    questions = Question.query.all()
    questions_data = [
        {
            'question_text': question.question_text,
            'options': question.options,
            'answer': question.answer
        }
        for question in questions
    ]
    print(questions_data)
   
    return render_template('quiz.html', questions=questions_data, quiz=quiz)

@app.route('/quiz/<int:quiz_id>/submit', methods=['POST'])
@login_required
def submit_quiz(quiz_id):
    """It handle user's submission of a quiz."""
    """Old submission logic for comparison purposes. May be deleted in future."""
    # user = current_user
    # score = 0
    # total_questions = 0

    # quiz = Quiz.query.get_or_404(quiz_id)
    # for question in quiz.questions:
    #     total_questions += 1
    #     selected_answer_id = request.form.get(f'question_{question.id}')

    #     if selected_answer_id:
    #         selected_answer = Answer.query.get(selected_answer_id)
    #         if selected_answer and selected_answer.is_correct:
    #             score += 1 

    # result = QuizResult(
    #     user_id=user.id,
    #     quiz_id=quiz_id,
    #     score=score,
    #     total_questions=total_questions,
    # )
    # db.session.add(result)
    # db.session.commit()
    # print(f'You scored {score} out of {total_questions}!')
    # return redirect(url_for('app.result', quiz_id=quiz_id))

@app.route('/quiz/<int:quiz_id>/result')
@login_required
def result(quiz_id):
    """It displays the result of a quiz"""
    score = request.args.get('score', type=int)
    total = request.args.get('total', type=int)
    if current_user.is_authenticated:
        quiz_result = QuizResult(user_id=current_user.id, quiz_id=quiz_id, score=score, total_questions=total)
        db.session.add(quiz_result)
        db.session.commit()
    
    return render_template('result.html', score=score, total=total)

if __name__ == '__main__':
    from app import create_app
    app_instance = create_app()
    app_instance.run(debug=True)
    
