"""
Schemas Pydantic da aplicação.

Centraliza todos os modelos de dados (request/response) em um único lugar.
"""

from enum import StrEnum

from pydantic import BaseModel, Field

# =============================================================================
# Operações matemáticas
# =============================================================================


class TipoOperacao(StrEnum):
    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"


class Numeros(BaseModel):
    numero1: int
    numero2: int


class ResultadoOperacao(BaseModel):
    resultado: float


# =============================================================================
# LLM / Histórias
# =============================================================================


class Historia(BaseModel):
    tema: str = Field(..., description="O tema da história a ser gerada")


class HistoriaResponse(BaseModel):
    historia: str = Field(..., description="A história gerada pela IA")


# =============================================================================
# Autenticação JWT
# =============================================================================


class Token(BaseModel):
    """Resposta do endpoint POST /token."""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Dados extraídos do payload do JWT após decodificá-lo."""

    username: str | None = None


class User(BaseModel):
    """Dados públicos do usuário (sem senha)."""

    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    """Usuário como está salvo no banco — inclui o hash da senha."""

    hashed_password: str
