import os
import secrets
import gnupg
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_cors import CORS 

load_dotenv()

# Path to React build
FRONTEND_BUILD_DIR = os.path.join(os.getcwd(), "Frontend", "dist")

# 1. Setup Flask app
app = Flask(__name__, static_folder="Frontend/dist/assets", static_url_path="/assets")
app.secret_key = "supersecret"  # Needed for sessions if you use them
CORS(app)


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

# ---- Register API ----
@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    pgp_key = request.form.get("pgp_key")

    if not username or not pgp_key:
        return jsonify({"error": "❌ Missing fields"}), 400

    # Check if username OR PGP key already exists
    existing_user = User.query.filter(
        (User.username == username) | (User.pgp_public_key == pgp_key)
    ).first()

    if existing_user:
        return jsonify({"error": "⚠️ Username or key already exists"}), 400

    try:
        new_user = User(username=username, pgp_public_key=pgp_key)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "✅ Registration successful!"}), 200
    except Exception:
        db.session.rollback()
        return jsonify({"error": "❌ Registration failed"}), 500

# ---- Login Step 1: Challenge ----
@app.route("/auth/challenge", methods=["POST"])
def auth_challenge():
    username = request.form.get("username")
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "❌ User not found"}), 404

    # Generate random one-time challenge
    challenge = secrets.token_hex(16)
    challenges[username] = challenge
    return jsonify({"challenge": challenge})

# ---- Login Step 2: Verify ----
@app.route("/auth/verify", methods=["POST"])
def auth_verify():
    username = request.form.get("username")
    signature_text = request.form.get("signature")  # pasted PGP signature text

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "❌ User not found"}), 404

    if username not in challenges:
        return jsonify({"error": "❌ No active challenge"}), 400

    challenge = challenges[username]

    if not signature_text:
        return jsonify({"error": "❌ No signature provided"}), 400

    # Import public key
    gpg.import_keys(user.pgp_public_key)

    # Save pasted signature into a temporary file
    sig_path = "temp_sig.asc"
    with open(sig_path, "w") as f:
        f.write(signature_text)

    # Verify signature against stored challenge
    try:
        verified = gpg.verify_data(sig_path, challenge.encode("utf-8"))
    finally:
        # Cleanup: remove temp file
        if os.path.exists(sig_path):
            os.remove(sig_path)

    if verified and verified.valid:
        del challenges[username]  # one-time use
        return jsonify({"message": f"✅ {username} authenticated successfully!"}), 200
    else:
        return jsonify({"error": "❌ Invalid signature"}), 400

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    if path != "" and os.path.exists(os.path.join(FRONTEND_BUILD_DIR, path)):
        return send_from_directory(FRONTEND_BUILD_DIR, path)
    else:
        return send_from_directory(FRONTEND_BUILD_DIR, "index.html")

# 4. CLI command to init DB
@app.cli.command("db_init")
def db_init():
    db.create_all()
    print("✅ Database initialized.")


# 5. Run the app
if __name__ == "__main__":
    app.run(debug=True)

