#!/usr/bin/env python
from app import create_app
from app.database import db
from app.models import Quiz, Question, Answer

app = create_app()

def add_dummy_data():
    """It adds tech-related dummy data to the database."""
    db.create_all()
    
    quiz = Quiz(title="Tech knowledge", description="A test of tech-related knowledge.")
    db.session.add(quiz)
    db.session.commit()
    question1 = Question(question_text='What does CPU stand for?', quiz_id=quiz.id)
    question2 = Question(question_text="Which programming language is used for web development?", quiz_id=quiz.id)
    db.session.add_all([question1, question2])
    db.session.commit()
    
    answer1 = Answer(answer_text="Central Processing Unit", is_correct=True, question_id=question1.id)
    answer2 = Answer(answer_text="Central Programming Unit", is_correct=False, question_id=question1.id)

    answer3 = Answer(answer_text="Python", is_correct=True, question_id=question2.id)
    answer4 = Answer(answer_text="Microsoft word", is_correct=False, question_id=question2.id)
 
    db.session.add_all([answer1, answer2, answer3, answer4])
    db.session.commit()
    
    print('Tech-related dummy quiz data added to the database.')
    
    
if __name__ ==  "__main__":
    with app.app_context():
        add_dummy_data()