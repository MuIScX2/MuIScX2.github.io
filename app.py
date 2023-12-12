import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///hncdatabase.db")

# Make sure API key is set
@app.route("/")
def index():

    user_stock_info = db.execute(
        "SELECT Name, last_name,phone_number,id FROM USER")

    # Query the current cash of the use

    return render_template("index.html", user_stock_info=user_stock_info
                           )



@app.route("/p_info/<int:user_id>")
def p_info(user_id):
    # Assuming `db` is your database connection object
    user_stock_info = db.execute(
        "SELECT * FROM USER WHERE id = ?",user_id
    )

    # Check if the user_stock_info is not empty or handle the case when the user is not found

    return render_template("p_info.html", user_stock_info=user_stock_info)
@app.route("/Computer/")
def Computer():
    # Assuming `db` is your database connection object
    user_stock_info = db.execute(
        "SELECT * FROM USER JOIN user_computers ON USER.id = user_computers.user_id JOIN computer_info ON computer_info.id = user_computers.computer"
    )

    # Check if the user_stock_info is not empty or handle the case when the user is not found

    return render_template("Computer.html", user_stock_info=user_stock_info)
@app.route("/Computer/<int:user_id>")
def SelectComputer(user_id):
    # Assuming `db` is your database connection object
    user_stock_info = db.execute(
        "SELECT * FROM USER JOIN user_computers ON USER.id = user_computers.user_id JOIN computer_info ON computer_info.id = user_computers.computer WHERE USER.id = ?",user_id
    )

    # Check if the user_stock_info is not empty or handle the case when the user is not found

    return render_template("Computer.html", user_stock_info=user_stock_info)
@app.route("/Record/")
def Record():
    # Assuming `db` is your database connection object
    user_Record= db.execute(
        "SELECT * FROM Record JOIN USER ON USER.id = Record.user_id JOIN Problem ON Problem.id = Record.problem_id JOIN Operator ON Operator.id = Record.Operator_id JOIN Solution ON Solution.id = Record.solution_id "
    )

    # Check if the user_stock_info is not empty or handle the case when the user is not found

    return render_template("Record.html", user_stock_info=user_Record)
@app.route("/Record/<int:user_id>")
def SelectRecord(user_id):
    # Assuming `db` is your database connection object
    user_Record= db.execute(
        "SELECT * FROM Record JOIN USER ON USER.id = Record.user_id JOIN Problem ON Problem.id = Record.problem_id JOIN Operator ON Operator.id = Record.Operator_id JOIN Solution ON Solution.id = Record.solution_id WHERE USER.id = ?",user_id
    )

    # Check if the user_stock_info is not empty or handle the case when the user is not found

    return render_template("Record.html", user_stock_info=user_Record)
@app.route("/Solution/")
def Solution():
    user_Record= db.execute(
        "SELECT * FROM Solution JOIN Problem On Problem.id = Solution.Problem_id Join Computer_info ON Computer_info.id = Solution.computer_id Join Problem_type ON problem_type_id = Problem_type.id  ")


    return render_template("Solution.html", user_stock_info=user_Record)
@app.route("/Solution/<int:solution>")
def SelectSolution(solution):

    user_Record= db.execute(
        "SELECT * FROM Solution JOIN Problem On Problem.id = Solution.Problem_id Join Computer_info ON Computer_info.id = Solution.computer_id Join Problem_type ON problem_type_id = Problem_type.id  WHERE Solution.id = ?",solution
    )


    return render_template("Solution.html", user_stock_info=user_Record)

@app.route("/Operator/<operatorname>")
def SelectOperator(operatorname):

    user_Record= db.execute(
        "SELECT * FROM Operator Join Problem_type ON Problem_type_id =Problem_type.id WHERE Operator.name = ?",operatorname
    )


    return render_template("Operator.html", user_stock_info=user_Record)
@app.route("/Operator/")
def Operator():

    user_Record= db.execute(
        "SELECT * FROM Operator Join Problem_type ON Problem_type_id =Problem_type.id "
    )


    return render_template("Operator.html", user_stock_info=user_Record)

@app.route("/Finduser",methods=["GET", "POST"])
def Finduser():
    if request.method == "POST":

        input = request.form.get("username")
        if not request.form.get("username"):
            return apology("must provide username", 403)
        if input.isdigit():
            user_stock_info = db.execute("SELECT Name, last_name,phone_number,id FROM USER WHERE phone_number = ?",request.form.get("username"))
            return render_template("index.html", user_stock_info=user_stock_info)
        else:
            user_stock_info = db.execute("SELECT Name, last_name,phone_number,id FROM USER WHERE (Name = ? OR last_name = ?)",request.form.get("username"),request.form.get("username"))
            return render_template("index.html", user_stock_info=user_stock_info)

    return render_template("Finduser.html")

@app.route("/Findcomputer",methods=["GET", "POST"])
def Findcomputer():
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        user_stock_info = db.execute("SELECT * FROM USER JOIN user_computers ON USER.id = user_computers.user_id JOIN computer_info ON computer_info.id = user_computers.computer WHERE (computer_info.Type LIKE '%'|| ?|| '%' OR Make_from LIKE '%'|| ? || '%' OR serial_number LIKE '%'|| ? || '%')",request.form.get("username"),request.form.get("username"),request.form.get("username"))
        return render_template("Computer.html", user_stock_info=user_stock_info)

    return render_template("Findcomputer.html")

@app.route("/Findoperator",methods=["GET", "POST"])
def Findoperator():
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        user_stock_info = db.execute("SELECT * FROM Operator Join Problem_type ON Problem_type_id =Problem_type.id WHERE (name = ? OR last_name = ? OR text = ?)",request.form.get("username"),request.form.get("username"),request.form.get("username"))
        return render_template("Operator.html", user_stock_info=user_stock_info)

    return render_template("Findoperator.html")

@app.route("/Findproblem",methods=["GET", "POST"])
def Findproblem():
    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 403)

        user_stock_info = db.execute("SELECT * FROM Solution JOIN Problem On Problem.id = Solution.Problem_id Join Computer_info ON Computer_info.id = Solution.computer_id Join Problem_type ON problem_type_id = Problem_type.id  WHERE (problem LIKE '%'|| ?|| '%' OR Error_code = ? OR text = ?OR Type = ?OR Software = ?)",request.form.get("username"),request.form.get("username"),request.form.get("username"),request.form.get("username"),request.form.get("username"))
        return render_template("Solution.html", user_stock_info=user_stock_info)

    return render_template("Findproblem.html")

if __name__ == '__main__':
    app.run(debug=True, port=8001)