from flask import Blueprint
from src.presentation.api.v1.usuario.routes import usuario_bp

def register_v1_routes(app):
    api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

    api_v1.register_blueprint(usuario_bp)

    app.register_blueprint(api_v1)
