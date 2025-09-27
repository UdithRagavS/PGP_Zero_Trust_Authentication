import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

# 1. Setup Flask app
app = Flask(__name__)
app.secret_key = "supersecret"  # Needed for flash messages (change in production)

# Database URL:
# - If DATABASE_URL is set (for Postgres), use it
# - Else, fallback to SQLite file "app.db"
db_url = os.getenv("DATABASE_URL", "sqlite:///app.db")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# 2. Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    pgp_public_key = db.Column(db.Text, nullable=False)

# 3. Routes
@app.route("/")
def home():
    return render_template("home.html")

# Register route (form + saving user)
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        pgp_key = request.form.get("pgp_key")

        if not username or not pgp_key:
            flash("❌ Both fields are required!", "error")
            return redirect(url_for("register"))

        # Duplicate check in Python
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("⚠️ Username already exists!", "error")
            return redirect(url_for("register"))

        try:
            new_user = User(username=username, pgp_public_key=pgp_key)
            db.session.add(new_user)
            db.session.commit()
            flash(f"✅ User {username} registered successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash("❌ Database error: " + str(e), "error")

        return redirect(url_for("register"))

    return render_template("register.html")


# 4. CLI command to init DB
@app.cli.command("db_init")
def db_init():
    db.create_all()
    print("✅ Database initialized.")

# 5. Run the app
if __name__ == "__main__":
    app.run(debug=True)
