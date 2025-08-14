from fastapi import APIRouter, HTTPException
from bson import ObjectId
from pymongo.errors import PyMongoError
from database import DATABASE
from schema import ClientCreate, ClientUpdate
from serialize import convert_data

router = APIRouter()


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
# CREATE CLIENT
# ==============================
@router.post("/client")
async def create_client(data: ClientCreate):
    try:
        result = await DATABASE["clients"].insert_one(data.model_dump())
        return {"message": "Client ajouté", "id": str(result.inserted_id)}
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