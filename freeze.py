from flask import url_for
from flask_frozen import Freezer
from app import app, load_from_json

freezer = Freezer(app)

if __name__ == '__main__':
    freezer.freeze()