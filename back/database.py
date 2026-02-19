# backend/database.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# ------------------ Load environment variables ------------------
load_dotenv()  # loads .env automatically

# ------------------ MongoDB Connection ------------------
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://rohanvivot3lite5g_db_user:de6FjjjOm7NsBZv2@cluster0.0tw0cws.mongodb.net/?retryWrites=true&w=majority"
)

try:
    client = MongoClient(MONGO_URI)
    db = client["lostlink_ai"]
    items_col = db["items"]        # lost/found items
    users_col = db["users"]        # user info
    feedback_col = db["feedback"]  # user feedback

    # Test connection
    client.admin.command('ping')
    print("✅ MongoDB connected successfully.")

except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    raise e

# ------------------ Twilio Credentials ------------------
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE")  # your Twilio number

if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE):
    print("⚠️ Twilio credentials missing in .env")
else:
    print("✅ Twilio credentials loaded successfully")

# ------------------ Gemini API Key ------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("⚠️ Gemini API key missing in .env")
else:
    print("✅ Gemini API key loaded successfully")

# ------------------ Optional Helper ------------------
def get_collection(name: str):
    """Return a MongoDB collection by name."""
    return db[name]
