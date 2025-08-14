from decimal import Decimal
from typing import Optional
from datetime import date, time, datetime
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId

class AddProd(BaseModel):
    title: str
    price: int
    
    
    @field_validator('title', mode="before")
    def valid_title(cls, value):
        if not value:
            raise ValueError("veuillez saisir le titre")
        return value
    
class UpdateProd(BaseModel):
    title: Optional[str] = None
    price: Optional[int] = None
    



# ==============================
# ObjectId Support
# ==============================
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


# ==============================
# CLIENT
# ==============================
class ClientBase(BaseModel):
    nom: str
    prenoms: str
    telephone: str

    @field_validator("nom", "prenoms", "telephone", mode="before")
    def not_empty(cls, value, field):
        if not value or str(value).strip() == "":
            raise ValueError(f"Veuillez saisir {field.name}")
        return value


class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    nom: Optional[str] = None
    prenoms: Optional[str] = None
    telephone: Optional[str] = None


class ClientDB(ClientBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ==============================
# UTILISATEUR
# ==============================
class UtilisateurBase(BaseModel):
    nom_utilisateur: str
    mot_de_passe_hash: str
    est_administrateur: bool = False
    compte_actif: bool = True
    client_id: PyObjectId

    @field_validator("nom_utilisateur", "mot_de_passe_hash", mode="before")
    def not_empty(cls, value, field):
        if not value or str(value).strip() == "":
            raise ValueError(f"Veuillez saisir {field.name}")
        return value


class UtilisateurCreate(BaseModel):
    nom_utilisateur: str
    mot_de_passe_hash: str
    est_administrateur: bool = False
    compte_actif: bool = True
    client_id: str  

class UtilisateurUpdate(BaseModel):
    nom_utilisateur: Optional[str] = None
    mot_de_passe_hash: Optional[str] = None
    est_administrateur: Optional[bool] = None
    compte_actif: Optional[bool] = None
    client_id: Optional[str] = None


class UtilisateurDB(UtilisateurBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ==============================
# PESEE
# ==============================
class PeseeBase(BaseModel):
    code_pesee: str
    date_pesee_1: Optional[date] = None
    date_pesee_2: Optional[date] = None
    poids_1: Optional[Decimal] = None
    poids_2: Optional[Decimal] = None
    heure_pesee_1: Optional[time] = None
    heure_pesee_2: Optional[time] = None
    poids_net: Optional[Decimal] = None
    refraction: Optional[Decimal] = None
    poids_refracte: Optional[Decimal] = None
    mouvement: Optional[str] = None
    provenance: Optional[str] = None
    client: Optional[str] = None
    representant: Optional[str] = None
    transporteur: Optional[str] = None
    contenant_pesee: Optional[str] = None
    immatriculation: Optional[str] = None
    produit: Optional[str] = None
    prix_produit: Optional[Decimal] = None
    statut_pesee: Optional[str] = None
    motif_annulation: Optional[str] = None
    reference_piece: Optional[str] = None
    client_id: str 
    utilisateur_id: str 

    @field_validator("code_pesee", mode="before")
    def not_empty(cls, value):
        if not value or str(value).strip() == "":
            raise ValueError("Veuillez saisir le code pesée")
        return value


class PeseeCreate(PeseeBase):
    pass


class PeseeDB(PeseeBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
