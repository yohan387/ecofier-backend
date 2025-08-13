import datetime
from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pymongo.errors import PyMongoError

from database import DATABASE
from schema import AddProd, UpdateProd
from serialize import convert_data


app = FastAPI(
    title="TEST API"
)

@app.get('/products')
async def get_all():
    try:
        result =  await DATABASE['products'].find().to_list(None)
        return convert_data(result)
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail="Database erreur")


@app.get('/product/{id_product}')
async def get_one(id_product: str):
    try:
        product = await DATABASE['products'].find_one({'_id': ObjectId(id_product)})
        if not product:
            raise HTTPException(status_code=404, detail="Non trouvé")
        return convert_data(product)
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database erreur")


@app.post('/products')
async def add(data: AddProd):
    try:
        result = await DATABASE['products'].insert_one({
            'title': data.title, 
            'price': data.price
        })
        return {'message': "Ajouté", 'id': str(result.inserted_id)}
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database erreur")


@app.put('/product/{id_product}')
async def update(id_product: str, data: UpdateProd):
    try:
        update_data = data.model_dump(exclude_none=True)
        result = await DATABASE['products'].update_one(
            {'_id': ObjectId(id_product)},
            {'$set': update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Non trouvé")
        return {'message': "modifié"}
    except PyMongoError:
        raise HTTPException(status_code=500, detail="Database erreur")