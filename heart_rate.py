from flask import Flask
from flask_restful import Api
from routes import HeartRate, HeartSearch, Login
from flask_jwt_extended import JWTManager
from py_dotenv import read_dotenv
import os

envPath = os.path.join(os.path.dirname(__file__), '.env')
read_dotenv(envPath)
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = os.getenv("ACCESS_TOKEN_SECRET")
api = Api(app)
jwt = JWTManager(app)

api.add_resource(Login, "/auth")

api.add_resource(HeartRate, "/heart")

api.add_resource(HeartSearch, "/heart/<id>")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5050")