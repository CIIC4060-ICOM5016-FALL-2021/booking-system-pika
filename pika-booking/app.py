from flask import Flask, render_template
import os

app = Flask(__name__, instance_relative_config=True)

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

# Sign in
@app.route('/account/signup')
def signup():
    return "Signup"

# Login
@app.route('/account/login')
def login():
    return "Login"

# Users
@app.route('/user/<username>')
def profile(username):
    #... Logic goes here
    return "It's " + str(username) + " !"


if __name__ == "__main__":
    app.run(debug=True, host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 4444)))