from flask import Blueprint, render_template


app = Blueprint('app', __name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/register')
def register():
    return render_template('registration.html')


if __name__ == '__main__':
    app.run(debug=True)