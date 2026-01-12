from flask import Flask
from src.presentation.api.v1 import register_v1_routes

def create_app():
    app = Flask(__name__)

    # Configuración básica
    app.config["JSON_SORT_KEYS"] = False

    # Registrar rutas
    register_v1_routes(app)

    # Health check
    @app.route("/health", methods=["GET"])
    def health():
        return {"status": "ok"}, 200

    return app