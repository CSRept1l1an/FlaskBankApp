from flask import request, redirect, url_for


def deposit(conn, cursor):
    if request.method == 'POST':
        username = request.form.get('username')
        amount = float(request.form.get('amount', 0))

        if username and amount > 0:
            cursor.execute('SELECT * FROM users WHERE name=?', (username,))
            user = cursor.fetchone()

            if user:
                balance = float(user[3]) if user[3] else 0
                new_balance = balance + amount

                cursor.execute('UPDATE users SET balance=? WHERE name=?', (new_balance, username))
                conn.commit()
                return redirect(url_for('dashboard', username=username))

    return redirect(
        url_for('index'))


def withdraw(conn, cursor):
    if request.method == 'POST':
        username = request.form.get('username')
        amount = float(request.form.get('amount', 0))

        if username and amount > 0:
            cursor.execute('SELECT * FROM users WHERE name=?', (username,))
            user = cursor.fetchone()

            if user and user[3] >= amount:
                new_balance = user[3] - amount
                cursor.execute('UPDATE users SET balance=? WHERE name=?', (new_balance, username))
                conn.commit()
                return redirect(url_for('dashboard', username=username))

    return redirect(url_for('index'))


def logout():
    return redirect(url_for('index'))
