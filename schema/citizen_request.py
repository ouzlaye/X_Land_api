from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, List

class Document(BaseModel):
    nom: str
    type: str
    contenu_base64: str

class Coordonnees(BaseModel):
    A: List[float]
    B: List[float]
    C: Optional[List[float]] = None
    D: Optional[List[float]] = None

class CitizenRequestCreate(BaseModel):
    nomComplet: str
    telephone: str
    email: Optional[EmailStr]
    superficie: str
    nature: str
    situation: str
    coordonnees: Coordonnees
    documents: List[Document]
