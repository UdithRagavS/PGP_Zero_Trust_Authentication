# Zero-Trust Authentication with PGP

This project implements a passwordless login system using PGP digital signatures and tamper-proof audit logs.

## 🚀 Quickstart

Clone and set up:

```bash
git clone https://github.com/<your-username>/pgp_zero_trust_auth.git
cd pgp_zero_trust_auth
python -m venv .venv
.venv\Scripts\activate    # On Windows
# source .venv/bin/activate   # On Mac/Linux
pip install -r requirements.txt


## Database Options

- **SQLite (default)**  
  No configuration required. Runs out of the box using `app.db`.

- **PostgreSQL (optional)**  
  1. Create a database in Postgres:
     ```sql
     CREATE DATABASE pgp_auth;
     ```
  2. Update `.env` with your connection string:
     ```
     DATABASE_URL=postgresql+psycopg://postgres:yourpassword@localhost:5432/pgp_auth
     ```
  3. Initialize:
     ```bash
     python -m flask db_init
     ```