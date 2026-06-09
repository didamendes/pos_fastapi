"""
Utilitários da aplicação — integração com o LLM Groq.
"""

from groq import Groq

from api.config import get_settings
from api.models import Historia

settings = get_settings()

_groq_client = Groq(api_key=settings.groq_api_key)


def gerar_historia(historia: Historia) -> str:
    """
    Gera uma história sobre o tema fornecido usando o modelo LLM da Groq.

    Parâmetros
    ----------
    historia : Historia
        Objeto com o tema da história a ser gerada.

    Retorna
    -------
    str
        O texto da história gerada.
    """
    prompt = f"Escreva uma historia sobre o tema: {historia.tema}"
    chat_completion = _groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )
    return chat_completion.choices[0].message.content
