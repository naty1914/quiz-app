from app.database import db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    """Stores the details of a user."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    

class Quiz(db.Model):
    """It stores the details of a quiz. """
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    questions = relationship('Question', back_populates='quiz')

class Question(db.Model):
    """It stores the details of a question. """
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    options = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.String(255), nullable=False)
    quiz_id = db.Column(db.Integer, ForeignKey('quiz.id'), nullable=False)
    quiz = relationship('Quiz', back_populates='questions')

    def __repr__(self):
        return f'<Question {self.id}: {self.question_text}>'
    
    def get_options(self):
        """Return the options as a list instead of a comma-separated string."""
        return self.options.split(',')

class QuizResult(db.Model):
    """It stores the results of a quiz. """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)

    quiz = db.relationship('Quiz', backref='results')