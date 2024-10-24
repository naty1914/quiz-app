#!/usr/bin/env python
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Question, Quiz

app = create_app()
with app.app_context():
    Question.query.delete()
    Quiz.query.delete()
    db.create_all()
    quiz_title = 'Tech related Quiz'
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
            'question_text': 'What does CPU stand for?', 
            'options': 'Central Programming Unit,Central Processing Unit,Computer Processing Unit,Control Processing Unit', 
            'answer': 'Central Processing Unit'
        },
        {
            'question_text': 'Which company developed the Java programming language?', 
            'options': 'Sun Microsystems, Google, Microsoft, Oracle Corporation', 
            'answer': 'Sun Microsystems'
        },
        
        {
            'question_text': 'What is the main programming language used to develop Android apps?', 
            'options': 'Java,Python,C++,C#', 
            'answer': 'Java'
        },

        {
            'question_text': 'Which version control system is widely used in software development?', 
            'options': 'Git, SVN, Mercurial, Subversion', 
            'answer': 'Git'
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
