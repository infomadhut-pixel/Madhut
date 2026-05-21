import eventlet
import logging


eventlet.monkey_patch()

from app import create_app
from dotenv import load_dotenv
from app.extensions import socketio

load_dotenv()

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)
app = create_app()
socketio.init_app(app)

if __name__ == "__main__":
    socketio.run(app)
