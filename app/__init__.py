from flask import Flask
from .routes import routes
import yaml
import os

def load_config():
    config_path = os.path.join("config", "config.yaml")
    if not os.path.exists(config_path):
        raise FileNotFoundError("config.yaml not found in config/ folder")

    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def create_app():
    app = Flask(__name__)

    # Load config.yaml into app.config
    app.config["APP_CONFIG"] = load_config()

    # Register routes
    app.register_blueprint(routes)

    return app
