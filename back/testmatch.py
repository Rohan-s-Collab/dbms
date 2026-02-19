# test_ai_matcher.py
import os
from bson import ObjectId
from database import items_col
from ai_matcher import run_matching_pipeline, generate_qr_for_item

# ------------------ Sample Items ------------------
lost_item = {
    "item_name": "Black Wallet",
    "description": "Leather black wallet with ID cards",
    "location": "Library",
    "date": "2025-10-19",
    "time": "10:00",
    "type": "lost",
    "contact_info": "rohanpersonal286@gmail.com",  # your email for test
    "wants_call": False,
    "priority": True,
    "is_claimed": False
}

found_item = {
    "item_name": "Black Wallet",
    "description": "Found leather black wallet with some cards",
    "location": "Library",
    "date": "2025-10-19",
    "time": "11:00",
    "type": "found",
    "contact_info": "rohanpersonal286@gmail.com",  # your email for test
    "wants_call": False,
    "priority": True,
    "is_claimed": False
}

# ------------------ Insert Sample Items ------------------
lost_id = items_col.insert_one(lost_item).inserted_id
found_id = items_col.insert_one(found_item).inserted_id
print(f"Inserted Lost Item ID: {lost_id}")
print(f"Inserted Found Item ID: {found_id}")

# ------------------ Run Matching Pipeline ------------------
result = run_matching_pipeline(str(lost_id))
print("Matching Result:", result)

# ------------------ Generate QR Code ------------------
qr_data = generate_qr_for_item(str(lost_id))
print("QR Code Base64:", qr_data[:100], "...")  # print first 100 chars

# ------------------ Cleanup Test Items ------------------
items_col.delete_one({"_id": ObjectId(lost_id)})
items_col.delete_one({"_id": ObjectId(found_id)})
print("✅ Test items cleaned up")
