#!/usr/bin/env python
from app import create_app
from app.database import db
from app.models import Quiz, Question


app = create_app()
with app.app_context():
    Question.query.delete()
    Quiz.query.delete()
    db.session.commit()