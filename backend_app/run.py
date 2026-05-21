import eventlet
eventlet.monkey_patch()

import logging
import os

from app import create_app
from dotenv import load_dotenv
from app.extensions import socketio

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_DIR = os.path.join(BASE_DIR, "logs")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logging.info("Application Started")

app = create_app()

socketio.init_app(app)

if __name__ == "__main__":
    socketio.run(app)