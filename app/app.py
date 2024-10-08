from flask import Blueprint, render_template


app = Blueprint('app', __name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)