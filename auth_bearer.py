from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils import decode_jwt


def verify_jwt(jwtoken: str) -> bool:
    isTokenValid: bool = False

    try:
        payload = decode_jwt(jwtoken)
    except:
        payload = None
    if payload:
        isTokenValid = True

    return isTokenValid


class JWTBearer(HTTPBearer):
    def _init_(self, auto_error: bool = True):
        super(JWTBearer, self)._init_(auto_error=auto_error)

    async def _call_(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self)._call_(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Schéma d'authentification invalide.")
            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Jeton invalide ou expiré.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Code d'autorisation invalide.")