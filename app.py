import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy   # <-- fixed

# 1. Setup Flask app
app = Flask(__name__)

# Database URL:
# - If DATABASE_URL is set (for Postgres), use it
# - Else, fallback to SQLite file "app.db"
db_url = os.getenv("DATABASE_URL", "sqlite:///app.db")
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)   # <-- fixed

# 2. Define a simple model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)

# 3. Routes
@app.route("/")
def home():
    return jsonify({"message": "Hello, Zero-Trust World!"})

# 4. CLI command to init DB
@app.cli.command("db_init")
def db_init():
    db.create_all()
    print("✅ Database initialized.")

# 5. Run the app
if __name__ == "__main__":
    app.run(debug=True)
