from flask import Flask
from flask_cors import CORS

from backend.logger import logger
from backend.environment import Environment
from backend.endpoints.device import device_bp
from backend.endpoints.master import master_bp
from backend.endpoints.shared import shared_bp


def run():
    app = Flask(__name__)

    CORS(app)

    app.static_folder = f"{app.root_path}/frontend"

    app.register_blueprint(shared_bp)
    if Environment.is_master():
        logger.info("Initializing in master mode")
        app.register_blueprint(master_bp)
    else:
        logger.info("Initializing in device mode")
        app.register_blueprint(device_bp)

    logger.info(
        f"Running app{' in debug mode' if Environment.debug() else ''}..."
    )
    app.run(
        debug=Environment.debug(),
        port=5000 if Environment.is_master() else 5001,
        host="0.0.0.0",
        threaded=True
    )


if __name__ == "__main__":
    run()
