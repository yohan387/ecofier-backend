import time
from typing import Dict
import bcrypt
import jwt
from fastapi import Request, HTTPException
from database import DATABASE

db = DATABASE

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(mot_de_passe):
    pwd_bytes = mot_de_passe.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password


def verify_password(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed_password)


def sign_jwt(user_id: str) -> Dict[str, str]:
    payload = dict(user_id=user_id, exp=time.time() + ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {'token': token}


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except HTTPException as e:
        return {}




async def authenticate_user(email: str, password: str):
    user = await db.getByInDB(criter="email", data=email, projection={'_id': 0})
    if not user:
        return False
    if verify_password(password, user['password']):
        return user
    return False


async def get_current_user(request: Request):
    token = request.headers.get('Authorization')
    credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"}, )
    if token is None or not token.startswith("Bearer "):
        raise credentials_exception
    token = token[len("Bearer "):]
    credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except jwt.InvalidTokenError:
        raise credentials_exception
    user = await db.getByIdInDB(uid=user_id, projection={'_id': 0})
    if user is None:
        raise credentials_exception
    return user


def validate_signup(name, prenom, telephone, password, confpassword):
    errors = {}

    # Validation du nom
    if not name:
        errors['name'] = "Veuillez saisir votre nom"

    # Validation du prénom
    if not prenom:
        errors['prenom'] = "Veuillez saisir votre prénom"

    # Validation du téléphone
    if not telephone:
        errors['telephone'] = "Veuillez saisir votre numéro de téléphone"
    elif not telephone.isdigit():
        errors['telephone'] = "Veuillez saisir des chiffres uniquement"

    # Validation du mot de passe
    if not password:
        errors['password'] = "Veuillez saisir votre mot de passe"
    elif len(password) < 8:
        errors['password'] = "Votre mot de passe doit comporter au moins 8 caractères"

    if not confpassword:
        errors['confpassword'] = "Veuillez re-saisir votre mot de passe"
    elif password != confpassword:
        errors['confpassword'] = "Vos mots de passe ne correspondent pas"

    return errors


def validate_login(telephone, password):
    errors = {}
    if not telephone:
        errors['telephone'] = "Veuillez saisir votre adresse e-mail"


    if not password:
        errors['password'] = "Veuillez saisir votre mot de passe"

    return errors