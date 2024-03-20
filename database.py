from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def initialize_db(app):
    db.init_app(app)
    with app.app_context():
        from models import User  # Import the User model here
        db.create_all()
        if not User.query.filter_by(username='john').first():
            new_user1 = User(username='john', password='123', balance=5000)
            db.session.add(new_user1)
        if not User.query.filter_by(username='jane').first():
            new_user2 = User(username='jane', password='456', balance=8000)
            db.session.add(new_user2)
        db.session.commit()
