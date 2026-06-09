"""
Configurações centralizadas da aplicação.

Lê as variáveis de ambiente do arquivo .env via python-dotenv.
Use get_settings() para acessar as configurações em qualquer módulo.
"""

import os
from functools import lru_cache

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


class Settings:
    """Configurações da aplicação carregadas do ambiente."""

    # --- Segurança JWT ---
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # --- API ---
    api_token: str

    # --- Groq LLM ---
    groq_api_key: str

    def __init__(self) -> None:
        self.secret_key = os.getenv("SECRET_KEY", "")
        self.algorithm = "HS256"
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
        self.api_token = os.getenv("API_TOKEN", "")
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")


@lru_cache
def get_settings() -> Settings:
    """Retorna as configurações da aplicação (resultado é cacheado)."""
    return Settings()
