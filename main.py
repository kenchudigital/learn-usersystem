from flask import Flask, Response, request
import pandas as pd
import os

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# command: export FLASK_APP=main
# command: flask fun

app = Flask(__name__)

# A. Register


@app.route("/register/<email>/<password>/<name>")
def register(email, password, name):

    # Validation
    if email == "":
        return "Failed. Email must not be empty"
    if password == "":
        return "Failed. Password must not be password"
    if name == "":
        return "Failed. Name must not be password"

    # Actual
    if os.path.exists('user.csv'):
        df = pd.read_csv('user.csv')
        # check email exist or not
        check = df[df['email'] == email].sum()
        if check > 0:
            return "Failed. The email has been already exist!"
        else:
            df.append([
                {"email": email}, {"password": password}, {"name": name}
            ]).to_csv("user.csv", index=False)
            return "Success."
    # First time, creating the csv file
    else:
        df = pd.DataFrame(
            [[email, password, name]],
            columns=['email', 'password', 'name']
        )
        df.to_csv('user.csv', index=False)
        return "Success."


# B. Get the display name
@app.route("/get_display_name/<email>")
def get_display_name(email):
    df = pd.read_csv('user.csv')
    selected_rows = df[df['email'] == email]
    if len(selected_rows) > 0:
        return selected_rows.iloc[0]['name']
    else:
        return "Failed. No such email!"


# C. Login & Set Cookies
@app.route("/login/<email>/<password>")
def login(email, password):
    df = pd.read_csv("user.csv")
    validated = ((df['email'] == email) & (df['password'] == password)).sum() > 0

    if validated:
        # set cookies
        resp = Response("Success")
        resp.set_cookie("receipt", email)
        return resp
    else:
        return "Failed"


# D. Set Display Name - we will use cookie in this part
@app.route("/set_display_name/<name>")
def set_display_name(name):
    email = request.cookies['receipt']
    df = pd.read_csv('user.csv')
    df = df.set_index('email')
    df.loc[email, "name"] = name
    df.to_csv('user.csv')

# command: export FLASK_APP=main
# command: flask fun
