import os

import fastapi
from groq import Groq

from api.models import Historia

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def common_api_token(api_token: str):
    API_TOKEN = (str(os.getenv("API_TOKEN")),)
    if api_token != API_TOKEN:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail="Token inválido"
        )
    return {"api_token": api_token}


def gerar_historio(historia: Historia):

    prompt = f"Escreva uma historia sobre o tema: {historia.tema}"

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )

    return chat_completion.choices[0].message.content
