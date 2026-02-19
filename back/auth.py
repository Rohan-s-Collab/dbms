from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from database import users_col

# ---------- CONFIG ----------
SECRET_KEY = "supersecretkey123"  # change to your own secret key!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 3

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")


# ---------- HELPER FUNCTIONS ----------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_token(email: str):
    """Generate JWT token with expiration"""
    payload = {
        "sub": email,
        "exp": datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_user_by_email(email: str):
    return users_col.find_one({"email": email})


# ---------- LOGIN / SIGNUP ----------
@router.post("/api/login")
async def login(data: dict):
    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    user = get_user_by_email(email)

    # New user -> Signup
    if not user:
        if not name:
            raise HTTPException(status_code=400, detail="Name is required for signup")
        hashed_pwd = hash_password(password)
        new_user = {"name": name, "email": email, "password": hashed_pwd}
        users_col.insert_one(new_user)
        token = create_token(email)
        return {
            "message": "User registered successfully",
            "email": email,
            "name": name,
            "access_token": token
        }

    # Existing user -> Login
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_token(email)
    return {
        "message": "Login successful",
        "email": user["email"],
        "name": user["name"],
        "access_token": token
    }


# ---------- AUTH PROTECTION ----------
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Extract user info from JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"email": user["email"], "name": user["name"]}
