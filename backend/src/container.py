# Acá después vas a inyectar repos, usecases, servicios

from src.application.usecases.usuario.listar_usuarios import ListarUsuariosUseCase
from src.infrastructure.database.repositories.usuario_fake_repository import UsuarioFakeRepository

def build_listar_usuarios_usecase():
    repo = UsuarioFakeRepository()
    return ListarUsuariosUseCase(repo)
