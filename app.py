from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__, template_folder='template')

# Connect to Cloud SQL
db_config = {
    'host': os.environ.get('DB_HOST', '104.155.157.238'),
    'user': os.environ.get('DB_USER', 'appuser'),
    'password': os.environ.get('DB_PASSWORD', 'Praveen@123'),
    'database': os.environ.get('DB_NAME', 'user_management')
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("✅ Connected to DB")
            return conn
    except Error as e:
        print("❌ DB Connection Error:", e)
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/submit', methods=['POST'])
def api_submit():
    data = request.get_json()
    name = data.get('name')
    age = data.get('age')
    city = data.get('city')

    if not name or not age or not city:
        return jsonify({'error': 'All fields are required'}), 400

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (name, age, city) VALUES (%s, %s, %s)", (name, age, city))
            conn.commit()
            return jsonify({'message': 'User inserted'}), 200
        except Error as e:
            print("❌ Insert Error:", e)
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'DB connection failed'}), 500

@app.route('/api/users')
def get_users():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, age, city FROM users")
            rows = cursor.fetchall()
            result = [{'id': r[0], 'name': r[1], 'age': r[2], 'city': r[3]} for r in rows]
            return jsonify(result)
        except Error as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            conn.close()
    return jsonify({'error': 'DB connection failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
