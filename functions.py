import sqlite3
import random
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


def transfer(conn, cursor):
    if request.method == 'POST':
        username = request.form.get('username')
        destuser = request.form.get('destuser')
        amount = float(request.form.get('amount', 0))

        if username and destuser and amount > 0:
            try:
                cursor.execute('SELECT * FROM users WHERE name = ?', (username,))
                sender = cursor.fetchone()

                if sender and sender[3] >= amount:
                    cursor.execute('SELECT * FROM users WHERE name = ?', (destuser,))
                    recipient = cursor.fetchone()

                    if recipient:
                        cursor.execute('UPDATE users SET balance = balance - ? WHERE name = ?', (amount, username))
                        cursor.execute('UPDATE users SET balance = balance + ? WHERE name = ?', (amount, destuser))
                        conn.commit()
                        return redirect(url_for('dashboard', username=username))
                    else:
                        return "Recipient not found", 404
                else:
                    return "Insufficient balance", 400
            except ValueError:
                return "Invalid amount", 400
            except sqlite3.Error as e:
                return f"Database error: {e}", 500
        else:
            return "Missing fields or invalid amount", 400
    else:
        return "Invalid method", 405


def cardnum():
    """Generates a random 6-digit "card number" string."""
    digits = [str(x) for x in random.sample(range(0, 10), 6)]
    return "".join(digits)
