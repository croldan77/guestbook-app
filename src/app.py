from flask import Flask, request, jsonify, render_template, redirect  # Added redirect
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    """Crea conexión a la base de datos"""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),  # Added default
            user=os.getenv('MYSQL_USER', 'root'),       # Added default
            password=os.getenv('MYSQL_PASSWORD', ''),   # Added default
            database=os.getenv('MYSQL_DATABASE', 'guestbook_db')  # Added default
        )
        return connection
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

def init_db():
    """Crea la tabla si no existe"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS entries (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    message TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            print("✅ Tabla 'entries' creada/verificada")
        except Error as e:
            print(f"❌ Error creando tabla: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    else:
        print("❌ No se pudo conectar a la base de datos para inicializar")

@app.route('/')
def home():
    return redirect('/guestbook')

@app.route('/guestbook', methods=['GET', 'POST'])  # Combined route decorator
def handle_guestbook():
    """Maneja tanto GET como POST para /guestbook"""
    if request.method == 'GET':
        return get_entries()
    elif request.method == 'POST':
        return add_entry()

def get_entries():
    """Obtener todas las entradas"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Error de base de datos"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name, message, created_at FROM entries ORDER BY created_at DESC")
        entries = cursor.fetchall()
        
        # Para debugging
        print(f"📊 Entradas encontradas: {len(entries)}")
        
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify(entries)
        else:
            return render_template('index.html', entries=entries)
            
    except Error as e:
        print(f"❌ Error en GET: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def add_entry():
    """Agregar nueva entrada"""
    # Determinar el tipo de contenido
    is_json_request = request.is_json
    is_form_submission = 'name' in request.form
    
    if is_json_request:
        data = request.get_json()
        name = data.get('name', '').strip()
        message = data.get('message', '').strip()
    elif is_form_submission:
        name = request.form.get('name', '').strip()
        message = request.form.get('message', '').strip()
    else:
        name = ''
        message = ''

    # Validaciones
    if not name or not message:
        if is_json_request or not is_form_submission:
            return jsonify({"error": "Nombre y mensaje son requeridos"}), 400
        else:
            # Para formularios, redirigir con un mensaje de error
            return redirect('/guestbook?error=missing_fields')

    conn = get_db_connection()
    if not conn:
        if is_json_request:
            return jsonify({"error": "Error de base de datos"}), 500
        else:
            return redirect('/guestbook?error=database_error')
    
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (name, message) VALUES (%s, %s)", (name, message))
        conn.commit()
        
        # RESPUESTA DIFERENCIADA
        if is_json_request:
            return jsonify({"success": True, "message": "Entrada agregada"}), 201
        else:
            # Redirigir después de POST exitoso (patrón Post-Redirect-Get)
            return redirect('/guestbook')
            
    except Error as e:
        if is_json_request:
            return jsonify({"error": str(e)}), 500
        else:
            return redirect('/guestbook?error=insert_error')
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint no encontrado"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == '__main__':
    print("🚀 Iniciando Guestbook App...")
    print("🔍 Configuración cargada:")
    print(f"   Host: {os.getenv('MYSQL_HOST', 'localhost')}")
    print(f"   Usuario: {os.getenv('MYSQL_USER', 'root')}")
    print(f"   Base de datos: {os.getenv('MYSQL_DATABASE', 'guestbook_db')}")
    
    init_db()
    print("🌐 Servidor iniciando en http://0.0.0.0:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)