from fastapi import APIRouter, HTTPException, Query
from typing import List
from bson import ObjectId
from pymongo.errors import PyMongoError
from schema import PeseeCreate
from database import DATABASE
from serialize import convert_data

router = APIRouter()

@router.post("/pesees")
async def create_pesees(data: List[PeseeCreate]):
    """
    Ajouter plusieurs pesées en une seule requête.
    """
    try:
        insert_list = []

        for p in data:
            d = p.model_dump()

            # --- Conversion des IDs ---
            try:
                d["client_id"] = ObjectId(d["client_id"])
                d["utilisateur_id"] = ObjectId(d["utilisateur_id"])
            except Exception:
                raise HTTPException(status_code=400, detail="client_id ou utilisateur_id invalide")

            # --- Conversion Decimal -> float ---
            for key in ["poids_1","poids_2","poids_net","refraction","poids_refracte","prix_produit"]:
                if d.get(key) is not None:
                    d[key] = float(d[key])

            # --- Conversion date/time -> string ISO ---
            if d.get("date_pesee_1"):
                d["date_pesee_1"] = d["date_pesee_1"].isoformat()
            if d.get("date_pesee_2"):
                d["date_pesee_2"] = d["date_pesee_2"].isoformat()
            if d.get("heure_pesee_1"):
                d["heure_pesee_1"] = d["heure_pesee_1"].strftime("%H:%M:%S")
            if d.get("heure_pesee_2"):
                d["heure_pesee_2"] = d["heure_pesee_2"].strftime("%H:%M:%S")

            insert_list.append(d)

        # --- Insertion batch ---
        result = await DATABASE["pesees"].insert_many(insert_list)

        # --- Retour pour l'app ---
        return {
            "message": f"{len(result.inserted_ids)} pesées ajoutées",
            "ids": [str(i) for i in result.inserted_ids]
        }

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database erreur: {str(e)}")



@router.get("/pesees/client/{client_id}")
async def get_pesees_by_client(
    client_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500)
):
    """
    Récupère la liste des pesées pour un client donné avec pagination.
    - skip : nombre de documents à sauter (offset)
    - limit : nombre maximum de documents à retourner
    """
    try:
        # Vérification de l'ID
        try:
            client_obj_id = ObjectId(client_id)
        except Exception:
            raise HTTPException(status_code=400, detail="client_id invalide")

        # Requête Mongo
        cursor = DATABASE["pesees"].find({"client_id": client_obj_id}).skip(skip).limit(limit)
        result = await cursor.to_list(length=limit)

        # Conversion ObjectId en string
        return convert_data(result)

    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database erreur: {str(e)}")
