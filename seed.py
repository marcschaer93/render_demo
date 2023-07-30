"""Seed database with sample data from CSV Files."""

from csv import DictReader
from models import User, Message, Follows
from app import create_app, db

app = create_app()

def seed_database():
    with app.app_context():
        # Create the database tables
        db.drop_all()
        db.create_all()

        with open('generator/users.csv') as users:
            db.session.bulk_insert_mappings(User, DictReader(users))

        with open('generator/messages.csv') as messages:
            db.session.bulk_insert_mappings(Message, DictReader(messages))

        with open('generator/follows.csv') as follows:
            db.session.bulk_insert_mappings(Follows, DictReader(follows))

        db.session.commit()

        print("Database seeded successfully.")

if __name__ == "__main__":
    seed_database()

