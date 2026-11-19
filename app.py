"""API REST de laboratorio remediada bajo prácticas DevSecOps (Solo uso local)."""
import hmac
import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("practica.db")


def get_configured_api_key() -> str:
    """Obtiene la API Key exclusivamente desde variables de entorno."""
    return os.environ.get("API_KEY", "")


def init_db() -> None:
    """Inicializa la base SQLite y carga usuarios de prueba desde variables de entorno."""
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS users "
            "(id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
        )
        admin_pwd = os.environ.get("DEMO_ADMIN_PASSWORD")
        student_pwd = os.environ.get("DEMO_STUDENT_PASSWORD")
        if admin_pwd:
            conn.execute(
                "INSERT OR IGNORE INTO users (id, username, password) VALUES (?, ?, ?)",
                (1, "admin", admin_pwd),
            )
        if student_pwd:
            conn.execute(
                "INSERT OR IGNORE INTO users (id, username, password) VALUES (?, ?, ?)",
                (2, "estudiante", student_pwd),
            )


@app.get("/api/health")
def health():
    return jsonify(status="ok", service="API de práctica segura")


@app.get("/api/profile")
def profile():
    configured_key = get_configured_api_key()
    provided_key = request.headers.get("X-API-Key", "")
    if not configured_key or not hmac.compare_digest(provided_key, configured_key):
        return jsonify(error="No autorizado"), 401
    return jsonify(user="admin", message="Acceso autorizado mediante entorno seguro")


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", ""))
    password = str(data.get("password", ""))

    # Consulta SQL parametrizada para prevenir inyección SQL (CWE-89)
    query = "SELECT id, username FROM users WHERE username = ? AND password = ?"
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(query, (username, password)).fetchone()

    if row:
        return jsonify(message="Login correcto", user={"id": row[0], "username": row[1]})
    return jsonify(error="Credenciales inválidas"), 401


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
