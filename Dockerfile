# ---- FRONTEND BUILD ----
FROM node:18-alpine as frontend
WORKDIR /frontend
COPY Frontend/package*.json ./
RUN npm install
COPY Frontend/ .
RUN npm run build

# ---- BACKEND BUILD ----
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq-dev gcc gnupg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy frontend build output into backend container
COPY --from=frontend /frontend/dist ./Frontend/dist

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]