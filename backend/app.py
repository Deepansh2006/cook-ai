import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flask import Flask
from backend.db import init_db
from backend.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config['JSON_SORT_KEYS'] = False
    init_db(app)
    register_routes(app)
    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
