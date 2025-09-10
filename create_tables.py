from app import create_app, db

# This script is used by the Render Build Command to create the database tables.
# It ensures that our PostgreSQL database has the correct tables (User, Transaction, Budget)
# before the main application starts.

# Create an instance of the Flask application
app = create_app()

# An application context is required to interact with the database
# outside of a normal web request.
with app.app_context():
    print("Creating database tables...")
    
    # This command reads the models defined in app/models.py and creates
    # the corresponding tables in the connected database.
    db.create_all()
    
    print("Database tables created successfully.")
