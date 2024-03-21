import sqlite3

from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for)

from functions import deposit, withdraw

app = Flask(__name__)


def get_dbcon():
    conn = sqlite3.connect('bank.sqlite')
    cursor = conn.cursor()
    return conn, cursor


def close_dbcon(conn):
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn, cursor = get_dbcon()

        cursor.execute('SELECT * FROM users WHERE name=? AND password=?', (username, password))
        user = cursor.fetchone()

        close_dbcon(conn)

        if user:
            return redirect(url_for('dashboard', username=username))
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')


# Register page function
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        balance = request.form['balance']
        # cardnumber = request.form['cardNumber']

        conn, cursor = get_dbcon()
        cursor.execute('INSERT INTO users (name, password, balance) VALUES (?,?,?)', (username, password, balance))


@app.route('/deposit', methods=['POST'])
def deposit_route():
    conn = sqlite3.connect('bank.sqlite')
    cursor = conn.cursor()
    result = deposit(conn, cursor)
    conn.close()
    return result


@app.route('/withdraw', methods=['POST'])
def withdraw_route():
    conn = sqlite3.connect('bank.sqlite')
    cursor = conn.cursor()
    result = withdraw(conn, cursor)
    conn.close()
    return result


@app.route('/dashboard/<username>')
def dashboard(username):
    conn, cursor = get_dbcon()

    cursor.execute('SELECT balance FROM users WHERE name=?', (username,))
    result = cursor.fetchone()

    close_dbcon(conn)

    balance = result[0] if result else 0

    return render_template('dashboard.html', username=username, balance=balance)


if __name__ == '__main__':
    app.run(debug=True)
