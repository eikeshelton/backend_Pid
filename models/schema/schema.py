from pydantic import BaseModel, EmailStr, Field
from datetime import date,datetime,time
from typing import Optional,List

#classe abstrata 
class PessoaBase(BaseModel):
    nome_usuario: Optional[str] = None
    foto_perfil: Optional[str] = None
    bio: Optional[str] = None
    tipo_usuario: Optional[str] = None

class UsuarioCreate(PessoaBase):
    email: EmailStr
    login: str
    senha: str
    data_nascimento: date


class Login(BaseModel):
    login: str
    senha: str

class UsuarioUpdate(PessoaBase):
    pass

class UsuarioSelect(PessoaBase):
    seguidores: int
    seguidos: int

class LoginUpdate(Login):
    email: EmailStr
    id: int

class Credenciais(BaseModel):
    email: EmailStr
    senha: str

class UserResetPassword(BaseModel):
    email: EmailStr
    token: Optional[str] = None
    new_password: Optional[str] = None

class UserSearch(BaseModel):
    login: str

class UserSearchType(BaseModel):
    tipo_usuario:str

class RegistrarBusca(BaseModel):
    usuario_id: int
    pesquisado_id: int

class MensagemRecebida(BaseModel):
    remetente_id: int
    destinatario_id: int
    texto: str

class Mensagem(BaseModel):
    id: int
    remetente_id: int
    destinatario_id: int
    texto: str
    id_conversa:int


class ParceiroTreinoSchema(BaseModel):
    id_usuario: Optional[int] = None
    modalidade: str
    estado_codigo_ibge: int
    municipio_codigo_ibge: int
    dia_da_semana: Optional[str] = None
    local: Optional[str] = ""
    agrupamento_muscular: Optional[str] = None
    observacoes: Optional[str] = None
    horario: Optional[str] = None
    tempo_treino: Optional[time] = None
    sexo: Optional[str] = None
    datetime_registro: Optional[datetime] = None
    

class ParceiroTreinoResponse(ParceiroTreinoSchema):
    id: int
    nome_usuario: str
    foto_perfil: Optional[str] = None
    sexo_usuario: Optional[str] = None
    seguidores:int
    seguidos:int
    bio:Optional[str] = None
    login:str

    class Config:
        from_attributes = True
class SeguidoresCreate(BaseModel):
    id_seguidor: int
    id_seguido: int
class SeguidoresResponse(BaseModel):
    id: int
    id_seguidor: int
    id_seguido: int

    class Config:
        from_attributes = True

class FCMTokenUpdate(BaseModel):
    fcm_token: str
    id_usuario: int

class Conversas(BaseModel):
    foto_perfil:str
    remetente_id:int
    destinatario_id:int
    ultima_mensagem:str
class SeguidoresAcao(SeguidoresCreate):
    acao: str  


class GuiaCreate(BaseModel):
    titulo: str
    foto_url: str
    id_usuario:int
    foto_guia:str
    titulo_guia:str
    texto_guia:str
class GuiaResponse(BaseModel):
    id_guias: int
    titulo: str
    foto_url: str
    id_usuario: int
class AlimentoBase(BaseModel):
    id: int
    grupo: str
    descricao: str
    energia_kcal: float
    proteina_g: float
    carboidrato_g: float
    quantidade_g: int
    lipideos_g: float

class AlimentoCreate(AlimentoBase):
    pass

class AlimentoResponse(AlimentoBase):
    id: int

    class Config:
        from_attributes = True

class RefeicaoBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

class RefeicaoResponse(RefeicaoBase):
   id_refeicao: int


class RefeicaoCreate(RefeicaoBase):
    pass

class RefeicaoResponse(BaseModel):
    nome: str
    descricao: str | None
    id_refeicao: int

    class Config:
        model_validate = True
class AlimentoSchema(BaseModel):
    id_usuario:int
    refeicao_id: int
    quantidade:float
    alimento_id: int
    data:date

class RefeicaoResponseList(BaseModel):
    total_energia_kcal: float
    total_proteina_g: float
    total_carboidrato_g: float
    total_lipideos_g: float

class BuscaAlimento(BaseModel):
    id_usuario:int
    data:date

class CadastrarEvento(BaseModel):
    id:Optional[int]
    organizador_id:int
    nome:str
    descricao:Optional[str] = None
    data_inicio: date
    hora_inicio: time
    localizacao : str
    municipio_id:int
    quantidade_participantes: Optional[int] = 0


class EventoResponse(BaseModel):
    id: int
    nome: str
    quantidade_participantes: int
    interesse_declarado: bool

    class Config:
        from_attributes = True
class InteresseEvento(BaseModel):
    participante_id: int
    interesse_declarado: bool


# Schema de entrada para criação de um novo treinamento
class TreinamentoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    is_publico: Optional[bool] = False  # Para indicar se o treinamento é público

    class Config:
        from_attributes = True

# Schema de saída para visualização dos dados do treinamento
class Treinamento(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    dia_da_semana: Optional[str]
    is_publico: bool

    class Config:
        from_attributes = True

class ExercicioCreate(BaseModel):
    nome: str
    series: Optional[int]
    carga: Optional[int]
    nota:Optional[str]
    repeticoes: Optional[int]
    tempoDescanso: Optional[int] 
    id_exercicio:int
# Schema para visualização de um treinamento armazenado no banco de dados
class TreinamentoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    dia_da_semana: Optional[str]
    exercicios: List[ExercicioCreate]

    class Config:
        from_attributes = True

class TreinamentoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    dia_da_semana: Optional[str] = None

    class Config:
        from_attributes = True

class ExercicioBase(BaseModel):
    id: int
    nome: str
    descricao: str

class ExercicioPersonalizadoBase(BaseModel):
    treinamento_id: int
    api_exercicio_id: Optional[int]
    nome_exercicio: str
    notas: Optional[str] = None
    repeticoes: Optional[int] = None
    series: Optional[int] = None
    carga_kg: Optional[int] = None
    tempo_descanso_seg: Optional[int] = None

    class Config:
        from_attributes = True

class ExercicioPersonalizadoCreate(ExercicioPersonalizadoBase):
    pass  

class ExercicioPersonalizadoUpdate(ExercicioPersonalizadoBase):
    pass  

class ExercicioPersonalizado(ExercicioPersonalizadoBase):
    id: int

    class Config:
        from_attributes = True