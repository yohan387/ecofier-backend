from fastapi import APIRouter, HTTPException
from pymongo.errors import PyMongoError
from schema import LoginRequest, RegisterRequest
from database import DATABASE
from utils import get_password_hash, sign_jwt, verify_password

router = APIRouter()

@router.post("/login")
async def login(login_request: LoginRequest):
    try:
        user = await DATABASE["utilisateurs"].find_one({"telephone": login_request.username})
        if not user:
            raise HTTPException(status_code=401, detail="Utilisateur introuvable")

        if not verify_password(login_request.password, user["mot_de_passe_hash"]):
            raise HTTPException(status_code=401, detail="Mot de passe incorrect")

        token = sign_jwt({"sub": str(user["_id"])})
        return {"access_token": token, "token_type": "bearer"}
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database erreur")
    
@router.post("/register")
async def register(register_request: RegisterRequest):
    try:
        user = await DATABASE["utilisateurs"].find_one({"telephone": register_request.username})
        if user:
            raise HTTPException(status_code=400, detail="Utilisateur déjà existant")

        hashed_password = get_password_hash(register_request.password)
        new_user = {
            "nom_utilisateur": register_request.username,
            "mot_de_passe_hash": hashed_password,
            "telephone": register_request.phone
        }
        await DATABASE["utilisateurs"].insert_one(new_user)
        return {"message": "Utilisateur créé avec succès"}
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database erreur")
    

