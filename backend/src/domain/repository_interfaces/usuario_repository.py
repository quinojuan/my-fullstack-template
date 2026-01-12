from abc import ABC, abstractmethod

class UsuarioRepository(ABC):

    @abstractmethod
    def listar(self):
        pass
