from passlib.context import CryptContext
import hashlib

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


users_db = {}  # temp in-memory user store


def hash_password(password: str):
    sha = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(sha)


def verify_password(plain: str, hashed: str):
    sha = hashlib.sha256(plain.encode()).hexdigest()
    return pwd_context.verify(sha, hashed)
