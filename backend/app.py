import sys
from pathlib import Path
import os

# Fix import paths
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flask import Flask
from flask_cors import CORS
from backend.db import init_db
from backend.routes import register_routes


def create_app():
    app = Flask(__name__)
    
    # Enable CORS (important for frontend)
    CORS(app)

    app.config['JSON_SORT_KEYS'] = False

    init_db(app)
    register_routes(app)

    return app


app = create_app()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)