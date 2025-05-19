"""
Modèles pour l'authentification
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Modèle de base pour les utilisateurs"""
    email: EmailStr
    full_name: Optional[str] = None
    is_admin: bool = False

class UserCreate(UserBase):
    """Modèle pour la création d'un utilisateur"""
    password: str

class UserUpdate(BaseModel):
    """Modèle pour la mise à jour d'un utilisateur"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    """Modèle pour un utilisateur en base de données"""
    id: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserBase):
    """Modèle pour un utilisateur"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    """Modèle pour un token d'authentification"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Données contenues dans un token"""
    email: Optional[str] = None
    is_admin: bool = False
