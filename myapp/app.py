import os
import sqlite3
from flask import Flask, request, render_template

app = Flask(__name__)

def init_db():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
    db_path = os.path.join(BASE_DIR, 'users.db')       
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS flags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flag TEXT NOT NULL
                )''')

    c.execute("SELECT * FROM users WHERE username = 'admin'")
    if not c.fetchone():
        c.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')")

    c.execute("SELECT * FROM flags")
    if not c.fetchone():
        c.execute("INSERT INTO flags (flag) VALUES ('THM{sql_injection_success}')")

    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, 'users.db')
        conn = sqlite3.connect(db_path)
        c = conn.cursor()

        try:
            c.execute(query)
            result = c.fetchone()
            if result:
                c.execute("SELECT flag FROM flags LIMIT 1")
                flag_row = c.fetchone()
                flag = flag_row[0] if flag_row else "Flag tapılmadı"
                message = f"Login uğurlu! Flag: {flag}"
            else:
                message = "Login alınmadı!"
        except Exception as e:
            message = f"Xəta: {e}"
        conn.close()

    return render_template("login.html", message=message)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
