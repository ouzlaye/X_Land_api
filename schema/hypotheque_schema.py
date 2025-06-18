from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime
from enum import Enum

class StatutHypotheque(str, Enum):
    demande_deposee = "demande_deposee"
    analyse_fonciere = "analyse_fonciere"
    hypotheque_enregistree = "hypotheque_enregistree"
    levee_hypotheque = "levee_hypotheque"

class DossierHypothecaireCreate(BaseModel):
    numeroTitre: str = Field(..., example="TF-2041")
    nomBanque: str = Field(..., example="BNDE Sénégal")
    contactBanque: str = Field(..., example="correspondant@bnda.sn")
    montantGaranti: str = Field(..., example="25 000 000 FCFA")

class DossierHypothecaire(BaseModel):
    id: str
    numeroTitre: str
    nomBanque: str
    contactBanque: str
    montantGaranti: str
    dateDepot: datetime
    statut: StatutHypotheque
    alertesActives: bool


class TraceurHypothecaire(BaseModel):
    id: str
    numeroTitre: str
    nomBanque: str
    contactBanque: str
    montantGaranti: str
    dateDepot: datetime
    alertesActives: bool
