"""Schémas Pydantic pour le module de conservation foncière (titres, coordonnées, NICAD)."""


from pydantic import BaseModel, Field, validator, model_validator
from typing import Dict
import re

NICAD_REGEX = r"^\d{2}\d{1}\d{3}\d{2}\d{3}\d{5}$"  # Format: RR D AM CICR SSS PPPPP = 16 chiffres

class VerifyTitleRequest(BaseModel):
    numeroTitre: str | None = Field(None, example="TF-0001")
    nicad: str | None = Field(None, example="0123011300100428")

    @model_validator(mode="before")
    def validate_input(cls, values):
        numeroTitre, nicad = values.get("numeroTitre"), values.get("nicad")
        if not numeroTitre and not nicad:
            raise ValueError("Veuillez fournir soit un numeroTitre, soit un nicad.")
        if nicad and not re.fullmatch(r"\d{16}", nicad):
            raise ValueError("NICAD invalide. Il doit contenir exactement 16 chiffres.")
        return values
 


class CoordonneesModel(BaseModel):
    A: tuple[float, float]
    B: tuple[float, float]
    C: tuple[float, float]
    D: tuple[float, float]

class TitleFoncierModel(BaseModel):
    numeroTitre: str
    nicad: str
    designation: str
    situation: str
    superficie: str
    proprietaireInscrit: str
    modeAcquisition: str
    dateInscription: str
    nota: str  # Anciennement libre, mais on pourra formater l'historique ici
    hypotheque: str | None = None  # Nouveau champ
    coordonnees: CoordonneesModel


    @validator("nicad")
    def validate_nicad(cls, v):
        if not re.fullmatch(NICAD_REGEX, v):
            raise ValueError("NICAD invalide. Format attendu : 2+1+3+2+3+5 chiffres (16 caractères).")
        return v
