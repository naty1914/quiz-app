# Quiz-App

## Introduction
An engaging platform for testing knowledge across various topics,
with interactive quizzes, real-time feedback, and a dynamic, enjoyable
learning experience

## Project Screenshot
<img src="app/static/images/landingpage.png">

### Author(s) LinkedIn:
<p>
    <a href="https://www.linkedin.com/in/natnael-seifu/">LinkedIn Profile</a>
</p>

## Developer#
<p>
    <strong>Natnael Seifu</strong><br>
    Contact: <a href="mailto:natiseifu02@gmail.com.com">natiseiuf02@gmail.com</a>
</p>
## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)


## Overview
**Quiz App** is an interactive web-based application designed to help users test their knowledge with multiple-choice questions. Users can answer questions, track their scores, and see their performance in different quiz categories.

## Features
- User authentication (registration and login)
- Dynamic quiz selection based on categories
- Instant feedback on performance
- Scoring system and result display
- REST API for quizzes
- Responsive design for mobile and desktop

## Technologies Used
- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: SQLite or PostgreSQL
- **Version Control**: Git

## Installation
To set up the project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/naty1914/quiz-app.git
   cd quiz-app
 2. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables: Create a .env file in the root directory and add the following**
   ```bash
   FLASK_APP=app.py
   FLASK_ENV=development
   DATABASE_URL=sqlite:///your_database.db
   SECRET_KEY=your_secret_key
   ```

5. **Run the application:**
   ```bash
   flask run
   ```