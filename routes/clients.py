from datetime import datetime
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from pymongo.errors import PyMongoError
from database import DATABASE
from schema import  ClientUpdate, LoginRequest, RegisterClientRequest
from serialize import convert_data
from utils import get_password_hash, sign_jwt, verify_password

router = APIRouter()


# ==============================
# CREATE CLIENT
# ==============================
@router.post("/register-client")
async def register(register_request: RegisterClientRequest):
    try:
        # Vérifier unicité du téléphone
        client = await DATABASE["clients"].find_one({"telephone": register_request.telephone})
        if client:
            raise HTTPException(status_code=400, detail="Client déjà existant")

        # Hash du mot de passe
        hashed_password = get_password_hash(register_request.mot_de_passe_en_clair)

        # Document à insérer
        new_client_to_insert = {
            "nom": register_request.nom,
            "prenoms": register_request.prenoms,
            "telephone": register_request.telephone,
            "mot_de_passe_hash": hashed_password,
            "created_at": datetime.utcnow()
        }

        # Insertion
        result = await DATABASE["clients"].insert_one(new_client_to_insert)

        # Récupération du document inséré
        inserted_client = await DATABASE["clients"].find_one({"_id": result.inserted_id})

        # Génération du JWT
        token = sign_jwt({"sub": str(result.inserted_id)})

        return {
            "message": "Client enregistré avec succès",
            "data": convert_data(inserted_client),
            "access_token": token
        }

    except PyMongoError as e:
        # log l'erreur si tu as un logger
        raise HTTPException(status_code=500, detail="Database erreur")


# ==============================
# LOGIN CLIENT
# ==============================
@router.post("/login-client")
async def login(login_request: LoginRequest):
    try:
        client = await DATABASE["clients"].find_one({"telephone": login_request.telephone})
        if not client:
            raise HTTPException(status_code=401, detail="Client introuvable")

        if not verify_password(login_request.mot_de_passe_en_clair, client["mot_de_passe_hash"]):
            raise HTTPException(status_code=401, detail="Mot de passe incorrect")

       
        token = sign_jwt({"sub": str(client["_id"])})
        return {"access_token": token, "token_type": "bearer", "data": convert_data(client) }
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database erreur")
    


# ==============================
# GET ALL CLIENTS
# ==============================
@router.get("/clients")
async def get_all_clients():
    try:
        result = await DATABASE["clients"].find().to_list(None)
        return convert_data(result)
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database erreur")


# ==============================
# GET ONE CLIENT
# ==============================
@router.get("/clients/{client_id}")
async def get_one_client(client_id: str):
    try:
        client = await DATABASE["clients"].find_one({"_id": ObjectId(client_id)})
        if not client:
            raise HTTPException(status_code=404, detail="Client non trouvé")
        return convert_data(client)
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database erreur")




# ==============================
# UPDATE CLIENT
# ==============================
@router.put("/clients/{client_id}")
async def update_client(client_id: str, data: ClientUpdate):
    try:
        update_data = data.model_dump(exclude_none=True)
        result = await DATABASE["clients"].update_one(
            {"_id": ObjectId(client_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Client non trouvé")
        return {"message": "Client modifié"}
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database erreur")