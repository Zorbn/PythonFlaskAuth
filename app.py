from flask import Flask

from login_manager import login_manager
from encryption import bcrypt

from routes import routes_bp
from models import db


app = Flask(__name__)
app.register_blueprint(routes_bp)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

with open("secret.txt", "r") as file:
    app.config["SECRET_KEY"] = file.read()


if __name__ == "__main__":
    db.app = app
    db.init_app(app)
    db.create_all()  # Create all tables that don't exist yet

    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.run(debug=True)
