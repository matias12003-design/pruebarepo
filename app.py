from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Hello from CI/CD pipeline!",
        "version": "1.0.0"
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

# Endpoint vulnerable a SQL Injection (para que ZAP lo detecte)
@app.route('/api/users/<user_id>')
def get_user(user_id):
    # VULNERABILIDAD INTENCIONAL - NO usar en producción
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"  # SQL Injection!
    cursor.execute(query)
    return jsonify({"user_id": user_id})

# Endpoint sin autenticación (para que ZAP reporte)
@app.route('/api/admin')
def admin():
    return jsonify({"secret": "admin_password_123"})  # Info sensible expuesta

# Endpoint que acepta JSON
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    # Sin validación de entrada
    username = data.get('username', '')
    password = data.get('password', '')
    return jsonify({"message": f"Login attempt for {username}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)