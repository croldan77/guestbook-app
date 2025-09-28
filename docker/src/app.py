from flask import Flask, request, jsonify, render_template, redirect
import mysql.connector
from mysql.connector import Error
import os
import time

app = Flask(__name__)

def get_db_connection():
    """Create a database connection with retry mechanism for Docker"""
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST', 'localhost'),
                user=os.getenv('MYSQL_USER', 'root'),
                password=os.getenv('MYSQL_PASSWORD', ''),
                database=os.getenv('MYSQL_DATABASE', 'guestbook_db')
            )
            print("✅ MySQL connection established")
            return connection
        except Error as e:
            print(f"❌ Attempt {attempt + 1}/{max_retries}: MySQL connection error: {e}")
            if attempt < max_retries - 1:
                print(f"🕒 Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                raise e

def init_db():
    """Create the table if it does not exist"""
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
            print("✅ Table 'entries' created/verified")
        except Error as e:
            print(f"❌ Error creating table: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

@app.route('/')
def home():
    return redirect('/guestbook')

@app.route('/guestbook', methods=['GET', 'POST'])
def handle_guestbook():
    if request.method == 'GET':
        return get_entries()
    elif request.method == 'POST':
        return add_entry()

def get_entries():
    """Get all entries"""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database error"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT name, message, created_at FROM entries ORDER BY created_at DESC")
        entries = cursor.fetchall()
        
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify(entries)
        else:
            return render_template('index.html', entries=entries)
            
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def add_entry():
    """Add new record"""
    if request.is_json:
        data = request.get_json()
        name = data.get('name', '').strip()
        message = data.get('message', '').strip()
    else:
        name = request.form.get('name', '').strip()
        message = request.form.get('message', '').strip()

    if not name or not message:
        return jsonify({"error": "Name and message are required"}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database error"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO entries (name, message) VALUES (%s, %s)",
            (name, message)
        )
        conn.commit()
        
        if request.is_json:
            return jsonify({"success": True, "message": "Record added"}), 201
        else:
            return redirect('/guestbook')
            
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == '__main__':
    print("🚀 Starting Guestbook App...")
    print("🔍 Configuration:")
    print(f"   MySQL Host: {os.getenv('MYSQL_HOST', 'localhost')}")
    print(f"   MySQL Database: {os.getenv('MYSQL_DATABASE', 'guestbook_db')}")
    
    # Initialize database with retries
    init_db()
    
    # Run application
    app.run(debug=True, host='0.0.0.0', port=5000)