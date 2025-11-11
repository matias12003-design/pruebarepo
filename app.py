from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Middleware para agregar security headers
@app.after_request
def add_security_headers(response):
    # Arregla: X-Content-Type-Options Header Missing (LOW)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Arregla: Content Security Policy (CSP) Header Not Set (MEDIUM)
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; font-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'deny';"
    
    # Arregla: Permissions Policy Header Not Set (LOW)
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=(), payment=(), usb=(), magnetometer=(), gyroscope=(), speaker=()'
    
    # Arregla: Insufficient Site Isolation Against Spectre (LOW)
    response.headers['Cross-Origin-Resource-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    response.headers['Cross-Origin-Embedder-Policy'] = 'require-corp'
    
    # Arregla: Server Leaks Version Information (LOW)
    response.headers['Server'] = 'SecureServer'
    
    # Arregla: Storable and Cacheable Content (INFORMATIONAL)
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    # Headers adicionales de seguridad (bonus)
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    return response

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