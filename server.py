import os
from flask import Flask
from dotenv import load_dotenv
from db import db
from app import analysis_bp

load_dotenv()

app = Flask(__name__)

# Flask-SQLAlchemy config
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize db with app
db.init_app(app)

# Register the blueprint
app.register_blueprint(analysis_bp)

# Create tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    print("  Registered endpoints:")
    print("    GET  /analyze?algo=bubble_sort&n=1000&steps=10")
    print("    POST /save_analysis")
    print("    GET  /retrieve_analysis?id=1")
    print()
    app.run(port=3000, debug=True)
