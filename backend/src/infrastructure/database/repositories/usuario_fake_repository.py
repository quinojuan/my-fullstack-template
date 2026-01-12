class UsuarioFakeRepository:
  def listar(self):
    return [
      {"id": 1, "email": "test1@mail.com"},
      {"id": 2, "email": "test2@mail.com"}
    ]