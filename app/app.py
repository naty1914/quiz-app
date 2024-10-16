from flask import Blueprint, Response, abort, json, jsonify, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import  Question, Quiz, QuizResult, User


app = Blueprint('app', __name__)
@app.route('/')
def landingpage():
    """It renders the landingpage.html template."""
    return render_template('landingpage.html')

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
    user = current_user
    quiz_results = QuizResult.query.join(Quiz).filter(
        QuizResult.user_id == user.id,
        Quiz.id.isnot(None)
    ).order_by(QuizResult.id.desc()).limit(5).all()
    if not quiz_results:
        message = "No score yet, take a quiz!"
        return render_template('dashboard.html', user=user, message=message)
    
    return render_template('dashboard.html', user=user, quiz_results=quiz_results)

@app.route('/logout')
def logout():
    """It logs out the user."""
    print("logging out")
    logout_user()
    return redirect(url_for('app.landingpage'))


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
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
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
    user = current_user
    score = 0
    total_questions = 0

    quiz = Quiz.query.get_or_404(quiz_id)
    for question in quiz.questions:
        total_questions += 1
        selected_answer = request.form.get(f'question_{question.id}')

        if selected_answer == question.answer:
            score += 1 

    result = QuizResult(
        user_id=user.id,
        quiz_id=quiz_id,
        score=score,
        total_questions=total_questions,
    )
    db.session.add(result)
    db.session.commit()
    print(f'You scored {score} out of {total_questions}!')
    return redirect(url_for('app.result', quiz_id=quiz_id))

@app.route('/quiz/<int:quiz_id>/result')
@login_required
def result(quiz_id):
    """It displays the result of a quiz"""
    score = request.args.get('score', type=int)
    total = request.args.get('total', type=int)
    user_answers = request.args.get('userAnswers', type=str)
    user_answers_list = json.loads(user_answers) if user_answers else []
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    quiz_questions = []

    for question in questions:
        quiz_questions.append({
            'question_text': question.question_text,
            'options': question.options.split(','),
            'correct_answer': question.answer,
        })

    structured_answers = [
        {
            'question': quiz_questions[i]['question_text'],
            'user_answer': user_answers_list[i]['answer'],
            'correct_answer': quiz_questions[i]['correct_answer'],
            'options': quiz_questions[i]['options']
        } for i in range(len(user_answers_list))
    ]
    
    if current_user.is_authenticated:
        quiz_result = QuizResult(user_id=current_user.id, quiz_id=quiz_id, score=score, total_questions=total)
        db.session.add(quiz_result)
        db.session.commit()
    return render_template('result.html', score=score, total=total, user_answers=structured_answers)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_question():
    """It adds a new question to the database using the
    selected quiz.( Tech or General Knowledge)"""
    if request.method == 'POST':
        question_text = request.form['question_text']
        options = request.form['options']
        answer = request.form['answer']
        selected_quiz = request.form.get('quiz_title')
        
        if selected_quiz == 'tech':
            quiz_title = 'Tech related Quiz'
        else:
            quiz_title = 'General Knowledge'
        
        quiz = Quiz.query.filter_by(title=quiz_title).first()
        if quiz is None:
            quiz = Quiz(title=quiz_title)
            db.session.add(quiz)
            db.session.commit()
    
        existing_question = Question.query.filter_by(
            question_text=question_text, quiz_id=quiz.id
        ).first()
        if existing_question:
            print('Question already exists!', 'warning')
            return redirect(url_for('app.add_question'))
        new_question = Question(
            question_text=question_text,
            options=options,
            answer=answer,
            quiz_id=quiz.id
        )
        db.session.add(new_question)
        db.session.commit()
        print('Question added successfully to {}!'.format(quiz_title), 'success')
        return redirect(url_for('app.quizzes'))
    return render_template('add_question.html')



@app.route('/quizzes', methods=['Get'], strict_slashes=False)
def get_quizzes():
    """It returns all quizzes in JSON format."""
    quizzes = Quiz.query.all()
    return jsonify([{'id': quiz.id, 'title': quiz.title} for quiz in quizzes])


@app.route('/quizzes/<int:quiz_id>/questions', methods=['GET'], strict_slashes=False)
def get_quiz(quiz_id):
    """It returns the questions of a quiz in JSON format."""
    quiz = Quiz.query.get(quiz_id)
    if quiz is None:
        abort(404)
    questions = []
    for question in quiz.questions:
        questions.append({
            'question_text': question.question_text,
            'options': question.get_options(),
            'correct_answer': question.answer,
            'id': question.id
        })
    
    quiz_data = {
        'quiz_title': quiz.title,
        'questions': questions
    }   
    return Response(json.dumps(quiz_data, sort_keys=False, indent=4, separators=(',', ': ')), mimetype='application/json')
    

@app.route('/questions', methods=['POST'], strict_slashes=False)
def create_question():
    """It creates a new question in the database."""
    data = request.get_json()
    if not data  or not all(key in data for key in ['quiz_id', 'question_text', 'options', 'answer']):
        return jsonify({'message': 'Invali request data'}), 400
    try:
        new_question = Question(**data)
        new_question.options = ','.join(data['options'])
        db.session.add(new_question)
        db.session.commit()
        return jsonify({'message': 'Question added successfully!'}), 201
    except Exception as ex:
        return jsonify({'message': 'Error adding question:' + str(ex)}), 500
    



@app.route('/quizzes/<int:quiz_id>/questions/<int:question_id>', methods=['PUT'], strict_slashes=False)
def update_question(quiz_id, question_id):
    """It updates a question in the database using the quiz_id and question_id."""
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404
    
    q = Question.query.filter_by(id=question_id, quiz_id=quiz_id).first()
    if not q:
        return jsonify({'error': 'Question not found for the specified quiz'}), 404
    
    data = request.get_json()
    if 'question_text' in data:
        q.question_text = data['question_text']
    if 'options' in data:
        q.options = ','.join(data['options'])
    if 'answer' in data:
        q.answer = data['answer']
    
    db.session.commit()
    return jsonify({'message': f'Question in {quiz.title} updated successfully!'})


@app.route('/quizzes/<int:quiz_id>/questions/<int:question_id>', methods=['DELETE'], strict_slashes=False)
def delete_question(quiz_id, question_id):
    """It deletes a question from the database using the question_id."""
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    q = Question.query.filter_by(id=question_id, quiz_id=quiz_id).first()
    if not q:
        return jsonify({'error': 'Question not found for the specified quiz'}), 404

    db.session.delete(q)
    db.session.commit()
    return jsonify({'message': f'Question in {quiz.title} deleted successfully!'})


if __name__ == '__main__':
    from app import create_app
    app_instance = create_app()
    app_instance.run(debug=True)
    