from flask import (Flask,
                   render_template,
                   request,
                   redirect,
                   url_for)

app = Flask(__name__)

users = {
    'john': {
        'password': '123',
        'balance': 5000
    },
    'jane': {
        'password': '456',
        'balance': 8000
    }
}


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            return redirect(url_for('dashboard', username=username))
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('login.html')


@app.route('/dashboard/<username>')
def dashboard(username):
    balance = users[username]['balance']
    return render_template('dashboard.html', username=username, balance=balance)


@app.route('/deposit', methods=['POST'])
def deposit():
    username = request.form['username']
    amount = float(request.form['amount'])
    users[username]['balance'] += amount
    return redirect(url_for('dashboard', username=username))


@app.route('/withdraw', methods=['POST'])
def withdraw():
    username = request.form['username']
    amount = float(request.form['amount'])
    if users[username]['balance'] >= amount:
        users[username]['balance'] -= amount
    return redirect(url_for('dashboard', username=username))


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
