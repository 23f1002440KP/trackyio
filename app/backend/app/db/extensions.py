from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager 
from passlib.context import CryptContext

## increase the jwt token validity period

 
 ## Extensions
db = SQLAlchemy()
jwt = JWTManager()

pwd_context = CryptContext(
    schemes=['argon2'],
    deprecated="auto"
)


## Some helper functions for password hashing and verification 

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def needs_rehash(password_hash: str) -> bool:
    return pwd_context.needs_update(password_hash)


 