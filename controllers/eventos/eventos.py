from models.eventos.eventos import Eventos
from models.schema.schema import *


def cadastrar_evento(cadastro:CadastrarEvento):
    db_cadastro = Eventos(
        organizador_id = cadastro.organizador_id,
        nome = cadastro.nome,
        descricao = cadastro.descricao,
        data_inicio = cadastro.data_inicio,
        horario_inicio =cadastro.hora_inicio,
        localizacao = cadastro.localizacao
    )