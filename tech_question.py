#!/usr/bin/env python
from app import create_app
from app.database import db
from app.models import Quiz, Question, Answer

app = create_app()

def add_tech_questions():
    """It clears existing quiz data  and add tech-related questions
    to the database.
    """
    db.create_all()
   
    Answer.query.delete()
    Question.query.delete()
    Quiz.query.delete()
    db.session.commit()
   
    quiz = Quiz(title="Tech Knowledge", description="A quiz to test your tech knowledge.")
    db.session.add(quiz)
    db.session.commit()

    question1 = Question(question_text="What does CPU stand for?", quiz_id=quiz.id)
    question2 = Question(question_text="What is the main programming language used to develop Android apps?", quiz_id=quiz.id)
    question3 = Question(question_text="What does HTTP stand for?", quiz_id=quiz.id)
    question4 = Question(question_text="Which company developed the Java programming language?", quiz_id=quiz.id)
    question5 = Question(question_text="Which version control system is widely used in software development?", quiz_id=quiz.id)
    
    db.session.add_all([question1, question2, question3, question4, question5])
    db.session.commit()
    
    
    answer1_q1 = Answer(answer_text="Central Programming Unit", is_correct=False, question_id=question1.id)
    answer2_q1 = Answer(answer_text="Central Processing Unit", is_correct=True, question_id=question1.id)
    answer3_q1 = Answer(answer_text="Computer Processing Unit", is_correct=False, question_id=question1.id)
    answer4_q1 = Answer(answer_text="Control Processing Unit", is_correct=False, question_id=question1.id)

    db.session.add_all([answer1_q1, answer2_q1, answer3_q1, answer4_q1])

    answer1_q2 = Answer(answer_text="Java", is_correct=True, question_id=question2.id)
    answer2_q2 = Answer(answer_text="Swift", is_correct=False, question_id=question2.id)
    answer3_q2 = Answer(answer_text="Python", is_correct=False, question_id=question2.id)
    answer4_q2 = Answer(answer_text="C#", is_correct=False, question_id=question2.id)
    
    db.session.add_all([answer1_q2, answer2_q2, answer3_q2, answer4_q2])

    answer1_q3 = Answer(answer_text="HyperText Transfer Protocol", is_correct=True, question_id=question3.id)
    answer2_q3 = Answer(answer_text="Hyperlink Transmission Protocol", is_correct=False, question_id=question3.id)
    answer3_q3 = Answer(answer_text="HyperText Transfer Protocol Secure", is_correct=False, question_id=question3.id)
    answer4_q3 = Answer(answer_text="HyperText Translation Protocol", is_correct=False, question_id=question3.id)
    
    db.session.add_all([answer1_q3, answer2_q3, answer3_q3, answer4_q3])

    answer1_q4 = Answer(answer_text="Sun Microsystems", is_correct=True, question_id=question4.id)
    answer2_q4 = Answer(answer_text="Google", is_correct=False, question_id=question4.id)
    answer3_q4 = Answer(answer_text="Microsoft", is_correct=False, question_id=question4.id)
    answer4_q4 = Answer(answer_text="Oracle Corporation", is_correct=False, question_id=question4.id)
    
    db.session.add_all([answer1_q4, answer2_q4, answer3_q4, answer4_q4])
   
    
    answer1_q5 = Answer(answer_text="Mercurial", is_correct=False, question_id=question5.id)
    answer2_q5 = Answer(answer_text="Subversion", is_correct=False, question_id=question5.id)
    answer3_q5 = Answer(answer_text="Git", is_correct=True, question_id=question5.id)
    answer4_q5 = Answer(answer_text="Perforce", is_correct=False, question_id=question5.id)
    
    db.session.add_all([answer1_q5, answer2_q5, answer3_q5, answer4_q5])
    db.session.commit()

    print("Tech-related questions added successfully!")


if __name__ == "__main__":
    with app.app_context():
        add_tech_questions()
