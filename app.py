from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error

# Tell Flask to use the 'template' folder
app = Flask(__name__, template_folder='template')

# Cloud SQL (MySQL) Public IP configuration
db_config = {
    'host': '104.155.157.238',
    'user': 'appuser',
    'password': 'Praveen@123',
    'database': 'user_management'
}

# Function to get MySQL connection
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("✅ Connected to MySQL database!")
        return conn
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Getting form fields
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    address = request.form.get('address')
    phone = request.form.get('phonenumber')

    # Insert into database
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (name, email, password, address, phone)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, email, password, address, phone))
            conn.commit()
            print("✅ User inserted successfully!")
        except Error as e:
            print(f"❌ Error inserting user: {e}")
        finally:
            cursor.close()
            conn.close()

    return render_template("submitteddata.html", name=name)

@app.route('/getdata')
def getdata():
    conn = get_db_connection()
    rows = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows = cursor.fetchall()
        except Error as e:
            print(f"❌ Error fetching data: {e}")
        finally:
            cursor.close()
            conn.close()
    return render_template("get_data.html", rows=rows)

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        user_id = request.form['id']
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                conn.commit()
                print("✅ User deleted successfully!")
            except Error as e:
                print(f"❌ Error deleting user: {e}")
            finally:
                cursor.close()
                conn.close()
        return redirect(url_for('getdata'))
    return render_template("delete.html")

@app.route('/data')
def data():
    return render_template("data.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
