from flask import Blueprint, jsonify
from src.container import build_listar_usuarios_usecase

usuario_bp = Blueprint("usuario", __name__, url_prefix="/usuarios")

@usuario_bp.route("/", methods=["GET"])
def listar_usuarios():
    usecase = build_listar_usuarios_usecase()
    usuarios = usecase.execute()
    return jsonify(usuarios), 200