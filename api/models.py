from enum import Enum

from pydantic import BaseModel, Field


class TipoOperacao(str, Enum):
    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"


class Numeros(BaseModel):
    numero1: int
    numero2: int


class Historia(BaseModel):
    tema: str = Field(..., description="O tema da historia a ser gerada")
