#!/usr/bin/env python
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Question, Quiz

app = create_app()
with app.app_context():
    db.create_all()
    quiz_title = 'General Knowledge Quiz'
    existing_quiz = Quiz.query.filter_by(title=quiz_title).first()
    
    if existing_quiz is None:
        new_quiz = Quiz(title=quiz_title)
        db.session.add(new_quiz)
        db.session.commit()
        quiz_id = new_quiz.id
    else:
        quiz_id = existing_quiz.id
    new_questions = [
        {
            'question_text': 'What is the capital of France?', 
            'options': 'Berlin,Madrid,Paris,Rome', 
            'answer': 'Paris'
        },
        {
            'question_text': 'What is the largest planet in our solar system?', 
            'options': 'Earth,Mars,Jupiter,Saturn', 
            'answer': 'Jupiter'
        },
        {   'question_text': 'Who wrote "Hamlet"?', 
            'options': 'Charles Dickens,William Shakespeare,Mark Twain,Jane Austen', 
            'answer': 'William Shakespeare'
        },
        {
            'question_text': 'What is the chemical symbol for gold?', 
            'options': 'Au,Ag,Fe,Hg', 
            'answer': 'Au'
        },
        {
            'question_text': 'What year did the Titanic sink?', 
            'options': '1912,1905,1898,1920', 
            'answer': '1912'
        }
    ]

    for question_data in new_questions:
        existing_question = Question.query.filter_by(question_text=question_data['question_text']).first()
        if existing_question is None:
            new_question = Question(
                question_text=question_data['question_text'],
                options=question_data['options'],
                answer=question_data['answer'],
                quiz_id=quiz_id
            )
            db.session.add(new_question)
            print(f"Added question: {question_data['question_text']}")
        else:
            print(f"Question already exists: {question_data['question_text']}")
    db.session.commit()

    print("Questions processed successfully.")
