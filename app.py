import os
import secrets
import gnupg
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

# 1. Setup Flask app
app = Flask(__name__)
app.secret_key = "supersecret"  # Needed for flash messages (change in production)

# Temproary storage challenges 
challenges ={}

# Setup GPG
gpg = gnupg.GPG()

# Prevent sensitive pages from being cached by browsers/proxies
@app.after_request
def add_security_headers(response):
    # Prevent caching of pages that may contain sensitive data
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0, private"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    # Recommended security headers (optional but good)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    return response


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
    pgp_public_key = db.Column(db.Text, unique =True, nullable=False)

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
            flash("❌ Registration failed. Please try again.", "error")
            return redirect(url_for("register"))

        # Check if username OR PGP key already exists
        existing_user = User.query.filter(
            (User.username == username) | (User.pgp_public_key == pgp_key)
        ).first()

        if existing_user:
            # Generic message (no clue whether username or key is duplicate)
            flash("⚠️ Registration failed. Please try again.", "error")
            return redirect(url_for("register"))

        try:
            new_user = User(username=username, pgp_public_key=pgp_key)
            db.session.add(new_user)
            db.session.commit()
            flash("✅ Registration successful!", "success")
        except Exception:
            db.session.rollback()
            # Still give generic error
            flash("❌ Registration failed. Please try again.", "error")

        return redirect(url_for("register"))

    return render_template("register.html")

# Login route (For using the credentials and login with a challenge)
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

# ---- PGP Challenge-Response Auth ----
@app.route("/auth/challenge", methods=["POST"])
def auth_challenge():
    username = request.form.get("username")
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "❌ User not found"}), 404

    # Generate random challenge
    challenge = secrets.token_hex(16)
    challenges[username] = challenge  # store temporarily
    return jsonify({"challenge": challenge})

@app.route("/auth/verify", methods=["POST"])
def auth_verify():
    username = request.form.get("username")
    challenge = request.form.get("challenge")
    signature = request.form.get("signature")

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "❌ User not found"}), 404

    if username not in challenges or challenges[username] != challenge:
        return jsonify({"error": "❌ Invalid challenge"}), 400

    # Import public key for verification
    gpg.import_keys(user.pgp_public_key)

    # Verify signature
    verified = gpg.verify(signature)

    if verified and verified.valid:
        del challenges[username]  # one-time use
        return jsonify({"message": f"✅ {username} authenticated successfully!"})
    else:
        return jsonify({"error": "❌ Invalid signature"}), 400

# 4. CLI command to init DB
@app.cli.command("db_init")
def db_init():
    db.create_all()
    print("✅ Database initialized.")

# 5. Run the app
if __name__ == "__main__":
    app.run(debug=True)
