from datetime import datetime
from bson import ObjectId


def convert_data(data):
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            # Renommer _id en id
            new_key = 'id' if key == '_id' else key
            
            # Convertir ObjectId en chaîne de caractères
            if isinstance(value, ObjectId):
                new_data[new_key] = str(value)
            # Convertir datetime en chaîne de caractères au format ISO
            elif isinstance(value, datetime):
                new_data[new_key] = value.isoformat()
                
            
            # Si c'est un dict, appel récursif
            elif isinstance(value, dict):
                new_data[new_key] = convert_data(value)
            # Si c'est une liste, appliquer la conversion à chaque élément
            elif isinstance(value, list):
                new_data[new_key] = [convert_data(item) for item in value]
            else:
                new_data[new_key] = value
        
        return new_data
    elif isinstance(data, list):
        return [convert_data(item) for item in data ]
    return data