# 🔐 Zero-Trust Authentication with PGP

This project implements a **passwordless login system** using **PGP digital signatures**, built on **Zero-Trust principles**:  
- No passwords, no shared secrets  
- Every authentication attempt is cryptographically verifiable  
- Optional PostgreSQL backend for production use  
- Containerized with Docker for one-click setup  

---

## 🚀 Quickstart (Local Setup)

Clone and set up:

```bash
git clone https://github.com/UdithRagavS/PGP_Zero_Trust_Authentication.git
cd PGP_Zero_Trust_Authentication
python -m venv .venv
.venv\Scripts\activate     # On Windows
# source .venv/bin/activate   # On Mac/Linux
pip install -r requirements.txt
```
Initialize the database (first time only):

```bash
python -m flask db_init
```
Run the app:

```bash
python -m flask run
```
Visit in browser:

👉 http://127.0.0.1:5000/

---

## 🐳 Docker Setup (One-Click)

Build and run with Docker Compose:

```bash
docker compose up --build
```
This will:
- Spin up a PostgreSQL container
- Build and serve the Flask + React app on port 5000

Visit 👉 http://localhost:5000

---

## 🗄 Database Options

### SQLite (default)

- Runs out of the box with app.db
- Great for local testing

### PostgreSQL (production-ready)

1. Create the database:

```bash
CREATE DATABASE pgp_auth;
```
2. Update .env:

```Initialize
DATABASE_URL=postgresql+psycopg2://postgres:yourpassword@localhost:5432/pgp_auth
```

3. Initialize:

```bash
python -m flask db_init
```
---

## 🔑 GnuPG Setup

The app requires GnuPG installed and available in your PATH.

Check installation:

```bash
gpg --version
```

Generate a new PGP key:

```bash
gpg --full-generate-key
```

Export your public key (paste this into the Register page):

```bash 
gpg --armor --export your@email.com
```
---

##🔄 Authentication Flow

### 1. Register

- Go to /register
- Enter a username and paste your PGP public key
- On success, the user is saved in the database

### 2. Login

- Go to /login
- Enter your username and click Get Challenge
- Copy the challenge string into challenge.txt
- Sign it with your private key:
```bash
gpg --armor --detach-sign -u your@email.com -o challenge.txt.asc challenge.txt
```
- Open challenge.txt.asc and paste the contents into the login form
- Submit → app verifies signature against your stored public key
- On success: 🎉 you’re authenticated

---

## 📂 Project Structure

```bash
PGP_Zero_Trust_Authentication/
│── app.py                 # Flask app entrypoint
│── requirements.txt       # Python dependencies
│── Dockerfile             # Multi-stage build (Frontend + Backend)
│── docker-compose.yml     # One-click setup (Flask + Postgres)
│── .env.example           # Example environment variables
│── Frontend/              # React frontend (Vite + JSX)
│   ├── src/pages/         # Login, Register, Home components
│   ├── src/components/    # Shared UI components
│   └── dist/              # Production build (served by Flask)
│── instance/              # Local SQLite DB (if used)
└── README.md              # Project documentation
```
---

## 🧪 How to Test End-to-End

1. Run locally (Flask or Docker)
2. Register a new user with username + exported public key
3. Login:
   - Get challenge from app
   - Save it into challenge.txt
   - Sign using:
   ```bash
   gpg --armor --detach-sign -u your@email.com -o challenge.txt.asc challenge.txt
   ```
   - Copy contents of challenge.txt.asc into the login form
   - Submit
4. Verify:
   - If valid → ✅ login success
   - If invalid → ⚠️ vague error shown (“Invalid signature / try again later”)

---

## 🔮 Future Upgrades

This project is a foundation for exploring passwordless authentication. Some exciting future upgrades could include:

- **JWT & Session Management** → Issue JSON Web Tokens after successful login for secure API access.  
- **Role-Based Access Control (RBAC)** → Add user roles (admin, auditor, standard user) with permission boundaries.  
- **Blockchain-backed Audit Logs** → Log authentication events to Ethereum testnet or Hyperledger for tamper-proof auditing.  
- **Multi-Factor Authentication (MFA)** → Combine PGP login with another factor (TOTP, WebAuthn, or biometric).  
- **WebAuthn/FIDO2 Integration** → Extend beyond PGP for broader hardware key support (YubiKey, TouchID, Windows Hello).  
- **Key Revocation & Rotation** → Add a dashboard for revoking lost PGP keys and uploading new ones securely.  
- **UI/UX Improvements** → Polished frontend with animations, dashboards, and audit log viewer.  
- **Kubernetes Deployment** → Scale easily with Helm charts and cloud-native logging/monitoring.  
- **CI/CD Pipeline** → Add automated testing, linting, and GitHub Actions for deployment.  
- **Mobile Client** → A React Native app for mobile-based PGP login and push notifications.  

---

## 🙌 Contributing
Pull requests are welcome! For major changes:
1. Open an issue to discuss improvements
2. Fork and create a feature branch
3. Submit a PR 🚀

---

## ⚡ Summary

This project demonstrates a fully working Zero-Trust authentication model using PGP challenge-response:

- No passwords, no credential reuse
- Works with SQLite (default) or Postgres
- React + Flask full stack app
- Dockerized for portability

--- 

