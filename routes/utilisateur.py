from fastapi import APIRouter, Depends, HTTPException
from bson import ObjectId
from pymongo.errors import PyMongoError
from auth_bearer import JWTBearer
from schema import UtilisateurCreate, UtilisateurUpdate
from database import DATABASE
from serialize import convert_data
from utils import get_password_hash

router = APIRouter(dependencies=[Depends(JWTBearer())])

# ==============================
# CREATE UTILISATEUR
# ==============================
@router.post("/utilisateur")
async def create_utilisateur(data: UtilisateurCreate):
    try:
        insert_data = data.model_dump()
        # hash du mot de passe
        insert_data["mot_de_passe_hash"] = get_password_hash(insert_data.pop("mot_de_passe_en_clair"))
        insert_data["client_id"] = ObjectId(insert_data["client_id"])
        result = await DATABASE["utilisateurs"].insert_one(insert_data)
        return {"message": "Utilisateur ajouté", "id": str(result.inserted_id)}
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database erreur")
    

# ==============================
# GET ALL UTILISATEURS
# ==============================
@router.get("/utilisateurs")
async def get_all_utilisateurs():
    try:
        result = await DATABASE["utilisateurs"].find().to_list(None)
        return convert_data(result)
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database erreur")


# ==============================
# GET ONE UTILISATEUR
# ==============================
@router.get("/utilisateurs/{utilisateur_id}")
async def get_one_utilisateur(utilisateur_id: str):
    try:
        utilisateur = await DATABASE["utilisateurs"].find_one({"_id": ObjectId(utilisateur_id)})
        if not utilisateur:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return convert_data(utilisateur)
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database erreur")


# ==============================
# UPDATE UTILISATEUR
# ==============================
@router.put("/utilisateurs/{utilisateur_id}")
async def update_utilisateur(utilisateur_id: str, data: UtilisateurUpdate):
    try:
        update_data = data.model_dump(exclude_none=True, exclude_unset=True)
        result = await DATABASE["utilisateurs"].update_one(
            {"_id": ObjectId(utilisateur_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
        return {"message": "Utilisateur modifié"}
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database erreur")
