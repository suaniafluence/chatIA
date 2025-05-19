"""
Routes d'authentification
"""
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.auth.models import User, UserCreate, Token
from app.auth.service import authenticate_user, create_access_token, get_current_active_user, create_user, get_admin_user
from app.config import settings

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Obtient un token d'accès pour l'authentification
    
    Args:
        form_data: Formulaire de connexion avec username (email) et password
        
    Returns:
        Token d'accès JWT
        
    Raises:
        HTTPException: Si les identifiants sont invalides
    """
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "is_admin": user.is_admin},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Récupère les informations de l'utilisateur courant
    
    Args:
        current_user: Utilisateur courant (injecté par la dépendance)
        
    Returns:
        Informations de l'utilisateur courant
    """
    return current_user

@router.post("/register", response_model=User)
async def register_user(user_create: UserCreate, admin_user: User = Depends(get_admin_user)):
    """
    Crée un nouvel utilisateur (réservé aux administrateurs)
    
    Args:
        user_create: Données pour la création de l'utilisateur
        admin_user: Utilisateur administrateur (injecté par la dépendance)
        
    Returns:
        L'utilisateur créé
        
    Raises:
        HTTPException: Si l'email est déjà utilisé
    """
    return await create_user(user_create)
