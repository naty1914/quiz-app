import os, sys
import unittest
from app import create_app, db
from app.models import User, Quiz, Question
from app.config import TestConfig
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class SimpleTestCase(unittest.TestCase):
    """A test case"""
    def setUp(self):
        """ It """
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()


        with self.app.app_context():
            db.drop_all()
            db.create_all()
            self.create_initial_data()

    def create_initial_data(self):
        """It create initial data for tests."""
        self.test_user = User(
            username='nati_user',
            email='nati@example.com',
            security_question='What is your mothers maiden name?',
            security_answer_hash='tsehay',
            avatar='avatar1.png'
        )

        self.test_user.set_password('testpassword')
        db.session.add(self.test_user)
        db.session.commit()

        self.quiz = Quiz(title='Simple Quiz')
        self.question2 = Question(question_text='What is the capital of France?', options='Berlin,Paris,London,Rome', answer='Paris', quiz=self.quiz)
        db.session.add(self.quiz)
        db.session.add(self.question2)
        db.session.commit()

    def test_home_page(self):
        """It tests the homepage loads correctly."""
        with self.app.app_context():
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Quiz App', response.data)

    def test_quiz_creation(self):
        """It tests creating a quiz."""
        with self.app.app_context():
            self.new_quiz = Quiz(title='Simple-Quiz 2')
            db.session.add(self.new_quiz)
            db.session.commit()

            quiz = Quiz.query.filter_by(title='Simple-Quiz 2').first()
            self.assertIsNotNone(quiz)
            self.assertEqual(quiz.title, 'Simple-Quiz 2')
            
    def test_user_creation(self):
        """It tests creating a user."""
        with self.app.app_context():
            new_user = User(username='test_user', email='test_user@example.com', security_question='What is your pet name?', security_answer_hash='test', avatar='avatar2.png')
            new_user.set_password('testpassword')
            db.session.add(new_user)
            db.session.commit()

            user = User.query.filter_by(email='test_user@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, 'test_user')

    def test_get_quizzes_category(self):
        """It tests fetching quizzes category via the API."""
        with self.app.app_context():
            response = self.client.get('http://127.0.0.1:5000/quizzes')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Simple Quiz', response.data)
    def test_get_quizzes_questions(self):
        """It tests fetching quizzes via the API."""
        with self.app.app_context():
            response = self.client.get('http://127.0.0.1:5000/quizzes/1/questions') 
           
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Simple Quiz', response.data)


if __name__ == '__main__':
    unittest.main()
