from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import db
from utils import create_error
import os

app = Flask(__name__)
CORS(app, resources={"*": {"origins": "*"}})
load_dotenv()

# Set up firebase connection
databaseURL = os.environ.get("DATABASE_URL")
firebase_key = {
    "type": os.environ.get("FIREBASE_TYPE"),
    "project_id": os.environ.get("FIREBASE_PROJECT_ID"),
    "private_key_id": os.environ.get("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.environ.get("FIREBASE_PRIVATE_KEY"),
    "client_email": os.environ.get("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.environ.get("FIREBASE_CLIENT_ID"),
    "auth_uri": os.environ.get("FIREBASE_AUTH_URI"),
    "token_uri": os.environ.get("FIREBASE_TOKEN_URI"),
    "auth_provider_x509_cert_url": os.environ.get("FIREBASE_AUTH_PROVIDER"),
    "client_x509_cert_url": os.environ.get("FIREBASE_CERT_URL")
}
cred_obj = firebase_admin.credentials.Certificate(firebase_key)
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': databaseURL
})


@app.route("/")
def index():
    return "Hello world"


@app.route("/stocks")
def get_available_stocks():
    ref = db.reference("/Stock/")
    data = ref.get(shallow=True)

    if data is None:
        return create_error("Error retrieving data")

    keys = list(data.keys())

    return {"stocks": keys}


@app.route("/stocks/<stock_ticker>")
def get_stock_data(stock_ticker):
    ref = db.reference(f"/Stock/{stock_ticker}")
    data = ref.get()

    if data is None:
        return create_error(f"No data found for {stock_ticker}", status=404)

    info = list(data.values())

    return {"stockSentimentData": info}
