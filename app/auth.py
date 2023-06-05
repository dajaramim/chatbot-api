import json
import logging
from typing import List


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jose.constants import ALGORITHMS
from motor.motor_asyncio import AsyncIOMotorClient

from app.config import keycloak_settings, dbclient


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=keycloak_settings.keycloak_url_token)

roles = json.loads(open("app/roles.json").read())


def has_permission(user_roles: List[str], resource: str, method: str) -> bool:
    for role in user_roles:
        if role in roles:
            if resource in roles[role]:
                if method in roles[role][resource]:
                    return True
    return False

def get_db(resource: str, method: str) -> AsyncIOMotorClient:
    def get_token_db(token: str = Depends(oauth2_scheme)) -> AsyncIOMotorClient:
        try:
            payload = jwt.decode(token, keycloak_settings.keycloak_public_key, algorithms=[ALGORITHMS.RS256],
                                options={"verify_signature": True, "verify_aud": False, "exp": True})
            logging.debug(payload)
            #username: str = payload.get("preferred_username")
            db_name: str = payload.get("bdName")
            #db_user: str = payload.get("bdUser")
            roles: List[str] = payload.get("resource_access")[keycloak_settings.keycloak_client_id]["roles"]
            #token_data = TokenData(username=username, db_name=db_name, db_user=db_user, roles=roles)

            if not has_permission(roles, resource, method):
                logging.error(f"Not enough permissions for {roles} to access {resource} with method {method}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not enough permissions",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError as err:
            logging.error(err)
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
            raise credentials_exception
        return dbclient[db_name]
    return get_token_db
