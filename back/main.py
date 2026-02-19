# backend

import os
import uuid
from datetime import datetime
from bson import ObjectId
from fastapi import (
    FastAPI, UploadFile, File, Form, Depends,
    HTTPException, BackgroundTasks
)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# -------------------- LOCAL IMPORTS --------------------
from database import items_col
from ai_matcher import run_matching_pipeline, generate_qr_for_item
from auth import router as auth_router, get_current_user
from notif import send_email, make_phone_call


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = FastAPI(title="LostLective Backend")
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")


@app.get("/api/items")
def get_items():
    try:
        items = list(items_col.find())
        result = []
        for i in items:
            result.append({
                "id": str(i["_id"]),
                "item_name": i.get("item_name", ""),
                "description": i.get("description", ""),
                "status": i.get("type", ""), 
                "category": i.get("category", ""),
                "location": i.get("location", ""),
                "date": i.get("date", ""),
                "image_url": i.get("image_url", "")
            })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/report_lost")
async def report_lost(
    background_tasks: BackgroundTasks,
    item_name: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    location: str = Form(...),
    contact_info: str = Form(...),
    priority: bool = Form(False),
    wants_call: bool = Form(False),
    image: UploadFile = File(None),
    user: dict = Depends(get_current_user)
):
    image_url = None
    if image:
        ext = os.path.splitext(image.filename)[1].lower()
        if ext not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
            raise HTTPException(status_code=400, detail="Unsupported file type.")
        filename = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            while chunk := await image.read(1024 * 1024):
                f.write(chunk)
        image_url = f"/uploads/{filename}"

    item = {
        "item_name": item_name,
        "description": description,
        "date": date,
        "time": time,
        "location": location,
        "contact_info": contact_info,
        "priority": priority,
        "wants_call": wants_call,
        "image_url": image_url,
        "type": "lost",
        "is_claimed": False,
        "email": user["email"]
    }

    result = items_col.insert_one(item)
    item_id = str(result.inserted_id)
    background_tasks.add_task(run_matching_pipeline, item_id)

    return {
        "message": "Lost item reported successfully",
        "item_id": item_id,
        "image_url": image_url,
        "qr_code": generate_qr_for_item(item_id)
    }


@app.post("/api/report_found")
async def report_found(
    background_tasks: BackgroundTasks,
    item_name: str = Form(...),
    description: str = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    location: str = Form(...),
    contact_info: str = Form(...),
    priority: bool = Form(False),
    image: UploadFile = File(None),
    user: dict = Depends(get_current_user)
):
    image_url = None
    if image:
        ext = os.path.splitext(image.filename)[1].lower()
        if ext not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
            raise HTTPException(status_code=400, detail="Unsupported file type.")
        filename = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            while chunk := await image.read(1024 * 1024):
                f.write(chunk)
        image_url = f"/uploads/{filename}"

    item = {
        "item_name": item_name,
        "description": description,
        "date": date,
        "time": time,
        "location": location,
        "contact_info": contact_info,
        "priority": priority,
        "image_url": image_url,
        "type": "found",
        "is_claimed": False,
        "email": user["email"]
    }

    result = items_col.insert_one(item)
    item_id = str(result.inserted_id)
    background_tasks.add_task(run_matching_pipeline, item_id)

    return {
        "message": "Found item reported successfully",
        "item_id": item_id,
        "image_url": image_url,
        "qr_code": generate_qr_for_item(item_id) 
    }


@app.post("/api/claim_item")
async def claim_item(background_tasks: BackgroundTasks, data: dict):
    item_id = data.get("item_id")
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    proof = data.get("proof")

    if not all([item_id, name, email, phone, proof]):
        raise HTTPException(status_code=400, detail="All fields are required")

    item = items_col.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    items_col.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": {
            "is_claimed": True,
            "claimed_by": {
                "name": name,
                "email": email,
                "phone": phone,
                "proof": proof,
                "claimed_at": datetime.utcnow().isoformat()
            }
        }}
    )

    owner_email = item.get("email")
    owner_phone = item.get("contact_info")
    item_name = item.get("item_name", "Unknown Item")

  
    if owner_email:
        subject = f"📦 Claim submitted for your item: {item_name}"
        body = f"""
Hello,

Someone has submitted a claim for your item "{item_name}" reported as {item.get('type').capitalize()}.

Claim Details:
- Name: {name}
- Email: {email}
- Phone: {phone}
- Proof: {proof}

Please review and contact the claimant directly if valid.

- Regards,
Rohan A M, Founder - LostLective
Reuniting lost items with their owners.
"""
        background_tasks.add_task(send_email, owner_email, subject, body)

    # Optional Twilio call
    if item.get("wants_call") and owner_phone:
        call_message = (
            f"Hello! This is LostLective. Someone has claimed your item {item_name}. "
            "Please check your email for details."
        )
        background_tasks.add_task(make_phone_call, owner_phone, call_message)

    # Confirmation email to claimant
    background_tasks.add_task(
        send_email,
        email,
        f"✅ Claim Received for {item_name}",
        f"Hi {name},\n\nYour claim for '{item_name}' has been received. "
        "The owner has been notified and may contact you soon.\n\n"
        "- Regards,\nRohan A M\nFounder - LostLective"
    )

    return {
        "message": "Claim submitted successfully. Owner has been notified.",
        "item_id": item_id,
        "notified_owner": bool(owner_email),
        "called_owner": bool(item.get("wants_call") and owner_phone)
    }

@app.get("/")
def root():
    return {"message": "LostLective Backend running ✅"}
