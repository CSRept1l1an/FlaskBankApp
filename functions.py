from app import db, User
from flask import request, redirect, url_for


def deposit():
    if request.method == 'POST':
        username = request.form['username']
        amount = float(request.form['amount'])
        user = User.query.filter_by(username=username).first()
        if user:
            user.balance += amount
            db.session.commit()
    return redirect(url_for('dashboard', username=username))


def withdraw():
    if request.method == 'POST':
        username = request.form['username']
        amount = float(request.form['amount'])
        user = User.query.filter_by(username=username).first()
        if user and user.balance >= amount:
            user.balance -= amount
            db.session.commit()
    return redirect(url_for('dashboard', username=username))


def logout():
    return redirect(url_for('index'))
