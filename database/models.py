from pydantic import BaseModel, validator
from typing import Dict, Tuple, Optional, List
import re
from enum import Enum

# Entrée de l'utilisateur
class TitleVerificationRequest(BaseModel):
    nicad: Optional[str] = None
    titleNumber: Optional[str] = None

    @validator("nicad")
    def validate_nicad(cls, v):
        if v and not re.match(r"^\d{16}$", v):
            raise ValueError("NICAD invalide : il doit contenir exactement 16 chiffres.")
        return v

# Sortie attendue
class LandRecordResponse(BaseModel):
    numeroTitre: str
    nicad: str
    designation: str
    situation: str
    superficie: str
    proprietaireInscrit: str
    modeAcquisition: str
    dateInscription: str
    nota: Optional[str]
    coordonnees: Dict[str, Tuple[float, float]]  # ex: {"A": (x, y), "B": ...}


# 
class CitoyenInfo(BaseModel):
    nom: str
    prenom: str
    telephone: str

class NouvelleDemandeRequest(BaseModel):
    citoyen: CitoyenInfo
    coordonnees: Dict[str, Tuple[float, float]]
    documents: List[str]  # fichiers simulés

class DemandeResponse(NouvelleDemandeRequest):
    id: str
    statut: str
    nicad: Optional[str] = None
    titreFoncierCree: bool = False
    deliberation_pdf: Optional[str] = None  # pour contenir le PDF de la délibération
    motifRefus: Optional[str] = None 


#modele de demande d'acte dgid
class TypeActe(str, Enum):
    bail_agricole = "bail_agricole"
    bail_habitation = "bail_habitation"
    titre_foncier = "titre_foncier"

class DemandeActeRequest(BaseModel):
    typeActe: TypeActe
