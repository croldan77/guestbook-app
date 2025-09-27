# test_mysql_connection.py
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

def test_mysql_connection():
    print("🔍 Testing MySQL connection...")
    print("=" * 40)
    
    # Load variables from .env
    load_dotenv()
    
    # Get settings
    config = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DATABASE', 'mysql')
    }
    
    print("📝 Configuration loaded:")
    print(f"  Host: {config['host']}")
    print(f"  User: {config['user']}")
    print(f"  Database: {config['database']}")
    print(f"  Password: {'***' if config['password'] else '(empty)'}")
    
    connection = None
    try:
        # Try to connect
        print("\n🔄 Connecting to the MySQL server...")
        connection = mysql.connector.connect(**config)
        
        # UPDATED VERIFICATION: Use the 'is_connected' property instead of the method
        if connection.is_connected():
            print("✅ ¡Connection successful!")
            
            # Retrieve server information using properties instead of methods
            server_info = connection.server_info  # Property, not method
            print(f"📊 MySQL server version: {server_info}")
            
            # Show current database
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE()")
            current_db = cursor.fetchone()[0]
            print(f"🗃️ Database connected: {current_db}")
            
            # Show current user
            cursor.execute("SELECT USER()")
            current_user = cursor.fetchone()[0]
            print(f"👤 Current user: {current_user}")
            
            # Check the connection status additionally
            print(f"🔌 Connection status: {'Connected' if connection.is_connected() else 'Offline'}")
            
            cursor.close()
            return True
            
    except Error as e:
        print(f"❌ Connection error: {e}")
        print("\n💡 Possible solutions:")
        print("  1. Check MySQL Service is running.")
        print("  2. Check the host, username, and password in the .env file.")
        print("  3. Make sure the user has the necessary connection permissions.")
        return False
        
    finally:
        if connection and connection.is_connected():
            connection.close()
            print("\n🔌 Connection closed successfully.")

def main():
    print("🔐 MYSQL CONNECTION TESTER")
    print("=" * 50)
    
    success = test_mysql_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎯 MySQL connection working correctly!")
    else:
        print("💥 MySQL connection error")
    
    return success

if __name__ == "__main__":
    main()