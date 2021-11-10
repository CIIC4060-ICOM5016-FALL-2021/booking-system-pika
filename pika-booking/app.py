from flask import Flask, render_template, request, jsonify
import os
from flask_cors import CORS
from controller.Person import Person

app = Flask(__name__, instance_relative_config=True)
CORS(app)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass


# Home Page, greeting
@app.route('/')
@app.route('/index')
@app.route('/home')
def main():
    return render_template('billie.html')


# About
@app.route('/about')
def about():
    return "This is an app"


# Contact
@app.route('/contact/')
def contacts():
    return "Contacts"


# User
@app.route('/users/<username>', methods=['GET', 'POST'])
def handle_users(username):
    if request.method == 'POST':
        return Person().create_new_person(request.json)
    else:
        return Person().get_all_persons()


@app.route('/users/<username>')
def profile(username):
    # ... Logic goes here
    return "It's " + str(username) + " !"


# Sign in
@app.route('/account/signup')
def signup():
    return "Signup"


# Login
@app.route('/account/login')
def login():
    return "Login"


if __name__ == "__main__":
    app.run(debug=True, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 4444)))
