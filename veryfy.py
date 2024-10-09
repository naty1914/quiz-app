#!/usr/bin/env python
from app import create_app
from app.database import db
from app.models import Quiz, Question, Answer

app = create_app()

def verify_data():

    quizzes = Quiz.query.all()
    if not quizzes:
        print('No quizzes found in the database.')
    else:
        for quiz in quizzes:
            print(f"Quiz: {quiz.title} - {quiz.description}")
            questions = Question.query.filter_by(quiz_id=quiz.id).all()
            print(f"Questions found: {len(questions)}")
            if not questions:
                print("  No questions found for this quiz.")
            for question in questions:
                print(f" * Question: {question.question_text}")
                answers = Answer.query.filter_by(question_id=question.id).all()
                if not answers:
                    print("   No answers found for this question.")
                for answer in answers:
                    print(f"  - Answer: {answer.answer_text} - {'Correct' if answer.is_correct else 'Incorrect'}")


if __name__ == "__main__":
    with app.app_context():
        verify_data()