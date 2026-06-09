"""
Router de autenticação JWT.

Fluxo:
  1. O usuário envia username + password para POST /token
  2. A API valida as credenciais e devolve um access_token (JWT)
  3. Nas próximas requisições, o usuário envia o token no cabeçalho:
       Authorization: Bearer <token>
  4. A API valida o token e identifica quem é o usuário
"""

from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.config import get_settings
from api.models import Token, User
from api.security import (
    autenticar_usuario,
    criar_access_token,
    fake_users_db,
    get_current_active_user,
)

settings = get_settings()
router = APIRouter()


@router.post(
    "/token",
    response_model=Token,
    summary="Login — obter token de acesso",
    description=(
        "Envie username e password para receber um JWT. Use esse token nos endpoints protegidos."
    ),
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    Autentica o usuário e retorna um token JWT.

    - Envie username e password no corpo (form-data)
    - O token retornado expira em 30 minutos por padrão
    - Use o token no cabeçalho: `Authorization: Bearer <token>`
    """
    usuario = autenticar_usuario(fake_users_db, form_data.username, form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = criar_access_token(
        dados={"sub": usuario.username},
        expira_em=timedelta(minutes=settings.access_token_expire_minutes),
    )
    return Token(access_token=token, token_type="bearer")


@router.get(
    "/users/me/",
    response_model=User,
    summary="Meu perfil",
    description="Retorna os dados do usuário atualmente autenticado.",
)
async def meu_perfil(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """Retorna os dados do usuário logado (requer token válido)."""
    return current_user


@router.get(
    "/users/me/items/",
    summary="Meus itens",
    description="Retorna a lista de itens pertencentes ao usuário autenticado.",
)
async def meus_itens(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> list[dict]:
    """Retorna os itens do usuário logado (requer token válido)."""
    return [{"item_id": "Foo", "owner": current_user.username}]
