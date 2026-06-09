"""
Camada de segurança da aplicação.

Responsável por:
- Hashing e verificação de senhas
- Criação e validação de tokens JWT
- Dependências FastAPI para autenticação (get_current_user, get_current_active_user)
"""

from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash

from api.config import get_settings
from api.models import TokenData, User, UserInDB

settings = get_settings()

# =============================================================================
# BANCO DE DADOS FALSO (apenas para testes/aprendizado)
# =============================================================================
# Em produção, substitua por uma consulta real ao banco de dados.
# A senha armazenada é sempre o HASH — nunca a senha em texto puro.
#
# Usuário de teste:
#   username: johndoe
#   password: secret
fake_users_db: dict[str, dict] = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": (
            "$argon2id$v=19$m=65536,t=3,p=4$wagCPXjifgvUFBzq4hqe3w"
            "$CYaIb8sB+wtD+Vu/P4uod1+Qof8h+1g7bbDlBID48Rc"
        ),
        "disabled": False,
    }
}

# =============================================================================
# HASHING DE SENHAS
# =============================================================================

password_hash = PasswordHash.recommended()

# Hash dummy para evitar timing attacks quando o usuário não existe.
# Sem isso, um atacante poderia descobrir usernames válidos medindo
# o tempo de resposta (usuários inválidos responderiam mais rápido).
DUMMY_HASH = password_hash.hash("dummypassword")

# Esquema OAuth2 — informa ao FastAPI onde fica o endpoint de login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def verificar_senha(senha_pura: str, senha_hash: str) -> bool:
    """Compara a senha digitada com o hash salvo no banco."""
    return password_hash.verify(senha_pura, senha_hash)


def gerar_hash_senha(senha: str) -> str:
    """Gera o hash de uma senha para armazenar no banco."""
    return password_hash.hash(senha)


# =============================================================================
# USUÁRIOS
# =============================================================================


def buscar_usuario(db: dict, username: str) -> UserInDB | None:
    """Busca um usuário no banco pelo username. Retorna None se não encontrar."""
    if username in db:
        return UserInDB(**db[username])
    return None


def autenticar_usuario(db: dict, username: str, password: str) -> UserInDB | bool:
    """
    Valida username e senha.

    Retorna o usuário se as credenciais forem válidas, False caso contrário.
    O DUMMY_HASH é verificado quando o usuário não existe para evitar
    timing attacks (resposta sempre leva o mesmo tempo).
    """
    usuario = buscar_usuario(db, username)
    if not usuario:
        verificar_senha(password, DUMMY_HASH)
        return False
    if not verificar_senha(password, usuario.hashed_password):
        return False
    return usuario


# =============================================================================
# JWT
# =============================================================================


def criar_access_token(dados: dict, expira_em: timedelta | None = None) -> str:
    """
    Cria e assina um JWT com os dados fornecidos.

    Parâmetros
    ----------
    dados : dict
        Informações a incluir no token (ex: {"sub": "johndoe"}).
    expira_em : timedelta, opcional
        Tempo até o token expirar. Padrão: 15 minutos.
    """
    payload = dados.copy()
    expiracao = datetime.now(UTC) + (expira_em or timedelta(minutes=15))
    payload.update({"exp": expiracao})
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


# =============================================================================
# DEPENDÊNCIAS FASTAPI
# =============================================================================


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """
    Dependência que valida o token JWT e retorna o usuário autenticado.

    Chamada automaticamente pelo FastAPI nos endpoints que usam
    Depends(get_current_user). Lança HTTP 401 se o token for inválido.
    """
    erro_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        # "sub" (subject) é o campo padrão do JWT que identifica o usuário
        username: str | None = payload.get("sub")
        if username is None:
            raise erro_credenciais
        token_data = TokenData(username=username)
    except InvalidTokenError as err:
        raise erro_credenciais from err

    usuario = buscar_usuario(fake_users_db, username=token_data.username)
    if usuario is None:
        raise erro_credenciais
    return usuario


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Dependência que garante que o usuário autenticado está ativo.

    Lança HTTP 400 se o usuário existir mas estiver com disabled=True.
    """
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo",
        )
    return current_user
