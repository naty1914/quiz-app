from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app import db
from app.models import Answer, Quiz, User


app = Blueprint('app', __name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
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
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
def logout():
    print("logging out")
    logout_user()
    return redirect(url_for('app.index'))


@app.route('/quiz_categories')
@login_required
def quizzes():
    quizzes = Quiz.query.all()
    return render_template('quiz_categories.html', quizzes=quizzes)

@app.route('/quiz/<int:quiz_id>')
@login_required
def quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('quiz.html', quiz=quiz)


if __name__ == '__main__':
    from app import create_app
    app_instance = create_app()
    app_instance.run(debug=True)
    
