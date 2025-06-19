import click
from app import create_app
from app.extensions import db
from app.models import User # Import the User model

# Create an app instance
app = create_app()

@app.cli.command("create-db")
def create_db():
    """Creates the database tables and seeds the admin user."""
    with app.app_context():
        db.create_all()
        print("Database tables created.")

        # Check if admin user exists
        if User.query.filter_by(role='admin').first() is None:
            # Create admin user
            admin = User(username='admin', role='admin')
            admin.set_password('admin123') # Set a secure password
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")
