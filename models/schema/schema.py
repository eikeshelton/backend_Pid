from pydantic import BaseModel, EmailStr
from datetime import date,datetime,time
from typing import Optional

# Definição das classes de dados usando Pydantic
class UsuarioCreate(BaseModel):
    email: EmailStr
    nome_usuario: str
    login: str
    senha: str
    tipo_usuario: str
    data_nascimento: date
    foto_perfil: bytes
    bio: str

class Login(BaseModel):
    login: str
    senha: str

class UsuarioUpdate(BaseModel):
    nome_usuario: Optional[str] = None
    foto_perfil: Optional[bytes] = None
    bio: Optional[str] = None
    tipo_usuario: Optional[str] = None

class UsuarioSelect(BaseModel):
    nome_usuario: str
    tipo_usuario: str
    foto_perfil: bytes
    bio: str
    seguidores: int
    seguidos: int

class LoginUpdate(BaseModel):
    login: str
    senha: str
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


class ParceiroTreino(BaseModel):
    modalidade: str
    estado_codigo_ibge: int
    municipio_codigo_ibge: int
    dia_da_semana: Optional[str] = None
    local: Optional[str] = ""
    agrupamento_muscular: Optional[str] = None
    observacoes: Optional[str] = None
    horario: Optional[time] = None
    tempo_treino: Optional[time] = None
    sexo: Optional[str] = None
    datetime_registro: Optional[datetime] = None
    id_usuario: Optional[int] = None





class ParceiroTreinoResponse(BaseModel):
    id: int
    id_usuario:int
    modalidade: str
    estado_codigo_ibge: int
    municipio_codigo_ibge: int
    local: Optional[str] = None
    horario: Optional[str] = None
    datetime_registro: datetime
    nome_usuario: str
    foto_perfil: Optional[str] = None
    sexo_usuario: Optional[str] = None
    seguidores:int
    seguidos:int
    bio:Optional[str] = None
    login:str

    class Config:
        from_attributes = True