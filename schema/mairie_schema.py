from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, List, Tuple, Literal
from datetime import datetime

# États métier pour simuler le cycle foncier complet
class StatutDemande(str, Enum):
    demande_soumise = "demande_soumise"
    instruction_locale = "instruction_locale"
    attente_nicad = "attente_nicad"
    nicad_refuse = "nicad_refuse"
    nicad_valide = "nicad_valide"
    deliberation_validee = "deliberation_validee"
    dossier_transmis_dgid = "dossier_transmis_dgid"
    instruction_dgid = "instruction_dgid"
    bail_emis = "bail_emis"
    bail_inscrit = "bail_inscrit"
    bail_en_vigueur = "bail_en_vigueur"
    bail_a_renouveler = "bail_a_renouveler"

#  Coordonnées cadastrales de la parcelle (format A→D)
class CoordonneesTerrain(BaseModel):
    A: Tuple[float, float]
    B: Tuple[float, float]
    C: Tuple[float, float]
    D: Tuple[float, float]

# Pièce justificative (facultatif) pour simuler des téléversements
class DocumentJoint(BaseModel):
    nom: str = Field(..., example="CNI_AliouSarr.pdf")
    type: Literal["identite", "justificatif_occupation", "deliberation", "nicad"] = "identite"
    contenu_base64: str  # ou url simulée plus tard

# Modèle d’entrée pour la soumission initiale de la demande
class DemandeFonciereCreate(BaseModel):
    nomComplet: str
    telephone: str
    email: Optional[str] = None
    superficie: str = Field(..., example="400 m²")
    nature: Literal["lot", "parcelle"] = Field(..., example="lot ou parcelle")
    situation: str = Field(..., example="Keur Massar Extension, près du marché central")
    coordonnees: CoordonneesTerrain
    documents: Optional[List[DocumentJoint]] = []

# Modèle complet d’une demande enregistrée (inclut ID, statut, timestamps, etc.)
class DemandeFonciere(BaseModel):
    id: str
    dateSoumission: datetime
    statut: StatutDemande
    nomComplet: str
    telephone: str
    email: Optional[str]
    superficie: str
    nature: str
    situation: str
    coordonnees: CoordonneesTerrain
    nicadAttribue: Optional[str] = None
    documents: Optional[List[DocumentJoint]] = []
    historiqueStatuts: Optional[List[Tuple[datetime, StatutDemande]]] = []
