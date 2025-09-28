# 🔐 Zero-Trust Authentication with PGP

This project implements a passwordless login system using **PGP digital signatures** and optional blockchain-backed audit logs.  
It is designed with **Zero-Trust principles**: no passwords, no shared secrets, and every authentication attempt is verifiable and tamper-proof.

---

## 🚀 Quickstart

Clone and set up:

```bash
git clone https://github.com/UdithRagavS/PGP_Zero_Trust_Authentication.git
cd PGP_Zero_Trust_Authentication
python -m venv .venv
.venv\Scripts\activate     # On Windows
# source .venv/bin/activate   # On Mac/Linux
pip install -r requirements.txt
```

---

## 🗄 Database Options

### SQLite (default)
No configuration required. Runs out of the box using `app.db`.

### PostgreSQL (optional)
1. Create a database in Postgres:
   ```sql
   CREATE DATABASE pgp_auth;
   ```
2. Update `.env` with your connection string:
   ```ini
   DATABASE_URL=postgresql+psycopg://postgres:yourpassword@localhost:5432/pgp_auth
   ```
3. Initialize the database:
   ```bash
   python -m flask db_init
   ```

---

## ▶️ Usage

Initialize the database (only first time):
```bash
python -m flask db_init
```

Run the app:
```bash
python -m flask run
```

Visit in browser:  
👉 http://127.0.0.1:5000/

Expected output: It will bring you to the home page where you can login or register as a new user.

---

## 🛠 Roadmap

- [✅] Add `/register` endpoint for uploading PGP public keys  
- [✅ ] Implement `/auth/challenge` and `/auth/verify` endpoints  
- [ ] Issue JWT tokens on successful login  
- [ ] Add tamper-proof blockchain-backed audit log (Ethereum testnet / Hyperledger)  
- [ ] Dockerize for one-click setup  
- [ ] Add unit tests (pytest)  
- [ ] Deploy demo on Render/Heroku for public testing  

---

## 🔑 GnuPG Setup

This project requires GnuPG installed and available in your system PATH.

Check installation:
```gpg --version
```

Generate a new PGP key:
```gpg --full-generate-key
```
Export your public key (to paste in the Register page):
```gpg --armor --export your@email.com
```
---

## 🔄 Authentication Flow

1. Register: 
- Go to /register
- Enter your username and paste your PGP public key
- User is saved in the database

2. Login:
- Go to /login
- Enter your username and click Get Challenge
- Copy the challenge string, save it to challenge.txt
- Sign it with your private key:
```gpg --clear-sign challenge.txt
```
- Open challenge.txt.asc, copy the signed message into the login form
- Submit → App verifies signature against stored public key
- On success, you’re authenticated 🎉

---

## 📂 Project Structure

```
PGP_Zero_Trust_Authentication/
│── app.py              # Flask app entrypoint
│── requirements.txt    # Python dependencies
│── .env.example        # Example environment variables
│── .gitignore          # Ignore secrets, venv, DB files
│── README.md           # Project documentation
│── templates/          # HTML Pages
│── instance/           # Local SQLite DB (auto-created if used)
└── .venv/              # Local virtual environment (ignored in git)
```

---

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first  
to discuss what you would like to change.
