from flask import Flask, render_template, url_for, request,  session, redirect, flash
import os
import json
from dotenv import load_dotenv
import re

load_dotenv()

base_dir = os.path.dirname(os.path.abspath(__file__))

json_file = os.path.join(base_dir, "users.json")



app = Flask(__name__,
            template_folder=os.path.join(base_dir, 'templates')
            ,static_folder=os.path.join(base_dir, "static"))
app.config["SECRET_KEY"] = os.environ.get("SESSION_KEY")


def load_data():
    if not os.path.exists("users.json"):
        return {}

    try:
        with open(json_file, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return{}


@app.route("/")

def landing_page():
    rendered_template = render_template("index.html")
    return rendered_template


@app.route("/login", methods =["GET", "POST"])
def login_page():
    j_file = load_data()
    users = j_file["users"]
    if request.method == "GET":
        rendered_template = render_template("login.html")
        return rendered_template
    
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = (request.form.get("password") or "").strip()
        if users[username] or users[username] != password:
            return render_template("login.html", error="Invalid username or password")
        elif users[username] and users[username] == password:
            session["username"] = username
            return redirect(url_for(dashboard_page), username=username)

@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    j_file = load_data()
    users = j_file["users"]
    if request.method == "GET":
        return render_template("signup.html")
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        if len(password) < 8:
            return render_template("signup.html", error="Password must be at least 8 characters long")
        elif password != request.form.get("confirm_password").strip():
            return render_template("signup.html", error="Passwords do not match")
        elif not re.search(r'[^A-Za-z0-9]', password):
            return render_template("signup.html", error="Password must contain at least one special character")
        elif not re.search(r"\d+", password):
            return render_template("signup.html", error="Password must contain at least one number")
        if users[username]:
            return render_template("signup.html", error="Username taken")
        else:
            try:
                with open("users.json", "w") as file:
                    j_file[username] = password
                    json.dump(j_file, file, indent=4, ensure_ascii=False)
            except IOError:
                return render_template("signup.html", error="Error saving user data")
            return redirect(url_for('login_page'), message="Signup Successful")

#placeholders below for planned routes

@app.route("/plant_homepage")

def plant_page():
    return render_template("plants.html")

@app.route("/cell_homepage")

def cell_page():
    return render_template("cells.html")

@app.route("/zoology_homepage")

def zoology_page():
    return render_template("zoology.html")

@app.route("/dashboard")
def dashboard_page():
    if "username" in session:
        return render_template("dashboard.html", username=session["username"], completed_articles=session["completed_articles"] if "completed_articles" in session else [])
    elif "username" not in session:
        return redirect(url_for("login_page"))

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html")

@app.route("/zoology_article1")

def zoology_article1():
    return render_template("ecologyintro.html")

@app.route("/zoology_article2")

def zoology_article2():
    return render_template("foodwebchain.html")

@app.route("/zoology_article3")

def zoology_article3():
    return render_template("evolution.html")

@app.route("/zoology_article4")

def zoology_article4():
    return render_template("taxonomy.html")

@app.route("/zoology_article5")

def zoology_article5():
    return render_template("lifeorigin.html")

@app.route("/cell_article1")

def cell_article1():
    return render_template("cellintro.html")

@app.route("/cell_article2")

def cell_article2():
    return render_template("cellstructure.html")

@app.route("/cell_article3")

def cell_article3():
    return render_template("dna_rna.html")

@app.route("/cell_article4")

def cell_article4():
    return render_template("meiomito.html")

@app.route("/cell_article5")

def cell_article5():
    return render_template("cellrespiration.html")

@app.route("/plant_article1")

def plant_article1():
    return render_template("plantintro.html")

@app.route("/plant_article2")

def plant_article2():
    return render_template("plantstructure.html")

@app.route("/plant_article3")

def plant_article3():
    return render_template("photosynthesis.html")

@app.route("/plant_article4")

def plant_article4():
    return render_template("plantreproduction.html")


if __name__ == "__main__":
    app.run(debug=True)
