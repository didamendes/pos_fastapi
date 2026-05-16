import os
from enum import Enum

from fastapi import FastAPI, HTTPException, Depends, status
from groq.types.chat import chat_completion
from pydantic import BaseModel, Field
from groq import Groq
from dotenv import load_dotenv
from rich import prompt

load_dotenv()

client = Groq(
    api_key= os.getenv("GROQ_API_KEY")
)


API_TOKEN = "123"


def common_api_token(api_token: str):
    if api_token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
        )
    return {"api_token": api_token}


app = FastAPI(dependencies=[Depends(common_api_token)])


@app.get("/teste")
def hello_world():
    return {"mensagem": " Hello World"}


@app.get(
    path="/soma/{numero1}/{numero2}",
    summary="Soma dois números inteiros",
    description="Recebe dois números inteiros e retorna a soma",
    tags=["Operações matemáticas"],
)
def soma(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


@app.post(
    path="/soma_formato2",
    summary="Soma dois números inteiros",
    description="Recebe dois números inteiros e retorna a soma",
    tags=["Operações matemáticas"],
)
def soma_formato2(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


class Numeros(BaseModel):
    numero1: int
    numero2: int


@app.post(
    path="/soma_formato3",
    summary="Soma dois números inteiros",
    description="Recebe dois números inteiros e retorna a soma",
    tags=["Operações matemáticas"],
    status_code=status.HTTP_200_OK,
    deprecated=True,
)
def soma_formato3(numeros: Numeros):
    total = numeros.numero1 + numeros.numero2
    return {"resultado": total}


class TipoOperacao(str, Enum):
    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"


@app.post("/operacao_matematica", tags=["Operações matemáticas"])
def operacao_matematica(numeros: Numeros, operacao: TipoOperacao):
    if operacao == TipoOperacao.soma:
        resultado = numeros.numero1 + numeros.numero2

    elif operacao == TipoOperacao.subtracao:
        resultado = numeros.numero1 - numeros.numero2

    elif operacao == TipoOperacao.multiplicacao:
        resultado = numeros.numero1 * numeros.numero2

    elif operacao == TipoOperacao.divisao:
        resultado = numeros.numero1 / numeros.numero2

    return {"resultado": resultado}


class Historia(BaseModel):
    tema: str = Field(..., description="O tema da historia a ser gerada")

@app.post("/gerar_historia")
def gerar_historia(historia: Historia):

    prompt = f'Escreva uma historia sobre o tema: {historia.tema}'

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )

    return { "historia": chat_completion.choices[0].message.content }