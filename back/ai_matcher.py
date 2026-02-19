# ai_matcher.py
import os
import re
import base64
import logging
from io import BytesIO

import qrcode
import google.generativeai as genai
from bson import ObjectId
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from database import items_col
from notif import send_email, make_phone_call

# ------------------ Logging ------------------
logger = logging.getLogger("LostLectiveAgent")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# ------------------ Gemini AI Config ------------------
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini_model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# ------------------ Validators ------------------
def is_valid_email(address: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", address))

# ------------------ QR Code Generator ------------------
def generate_qr_for_item(item_id: str) -> str:
    """Generate a QR code image string for the frontend."""
    base_url = os.getenv("BASE_URL", "http://localhost:5173")
    url = f"{base_url}/items/{item_id}"
    qr = qrcode.make(url)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

# ------------------ Notifications ------------------
def ai_agent_notify(lost_item: dict, found_item: dict):
    """Notify user via email and optionally phone call with QR code."""
    contact = lost_item.get("contact_info")
    item_id = str(found_item.get("_id"))
    base_url = os.getenv("BASE_URL", "http://localhost:5173")

    # Generate QR code
    qr_data = generate_qr_for_item(item_id)

    subject = "🎯 Possible Match for Your Lost Item!"
    body = f"""
Hi,<br><br>

We may have found a match for your lost item: <b>{lost_item['item_name']}</b>.<br><br>

Matched with found item:<br>
- Name: {found_item['item_name']}<br>
- Description: {found_item['description']}<br>
- Location: {found_item['location']}<br>
- Date & Time: {found_item['date']} {found_item['time']}<br><br>

You can view the item details by scanning the QR code below or clicking the link:<br>
<a href="{base_url}/items/{item_id}">
    <img src="{qr_data}" alt="View Item QR" width="200" height="200" />
</a><br><br>

Please log in to LostLective to confirm the match.<br><br>

– LostLective Agent 🤖<br>
Regards,<br>
Rohan A M<br>
Founder :: LostLective<br>
Reuniting Things One At A Time<br><br>

<small>DO NOT REPLY. THIS IS AUTO-GENERATED.</small>
"""

    # Send Email (HTML)
    if contact and is_valid_email(contact):
        try:
            from email.message import EmailMessage
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = os.getenv("EMAIL_USER")
            msg['To'] = contact
            msg.set_content("Please view this email in HTML-enabled client to see QR code and link.")
            msg.add_alternative(body, subtype='html')
            import smtplib
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
                smtp.send_message(msg)
            logger.info(f"✅ Email sent with QR code to {contact}")
        except Exception as e:
            logger.error(f"❌ Email sending failed: {e}")
    else:
        logger.warning(f"⚠️ Invalid or missing email: {contact}")

    # Optional phone call
    if lost_item.get("wants_call") and contact and contact.startswith("+"):
        try:
            call_message = f"Hello! A match is found for your lost item: {lost_item['item_name']} at {found_item['location']}. Check LostLective."
            make_phone_call(to_number=contact, message=call_message)
        except Exception as e:
            logger.error(f"📞 Call failed: {e}")

# ------------------ TF-IDF Matcher ------------------
def match_with_tfidf(new_item: dict, threshold: float = 0.75) -> list:
    """Return a list of TF-IDF matched items."""
    opposite_type = "found" if new_item["type"] == "lost" else "lost"
    all_items = list(items_col.find({"type": opposite_type, "is_claimed": False}))

    if not all_items:
        logger.info("No opposite-type items for TF-IDF matching.")
        return []

    descriptions = [item.get("description", "") for item in all_items]
    descriptions.append(new_item.get("description", ""))

    try:
        vectors = TfidfVectorizer().fit_transform(descriptions).toarray()
        similarities = cosine_similarity([vectors[-1]], vectors[:-1])[0]
    except Exception as e:
        logger.error(f"TF-IDF error: {e}")
        return []

    matches = []
    for idx, score in enumerate(similarities):
        if score >= threshold:
            matched_item = all_items[idx]
            logger.info(f"🔍 TF-IDF Match: {matched_item['item_name']} (Score: {score:.2f})")
            ai_agent_notify(matched_item, new_item)
            matches.append(matched_item)
    return matches

# ------------------ Gemini Matcher ------------------
def match_with_gemini(new_item: dict) -> list:
    """Return a list of Gemini AI matched items."""
    other_items = list(items_col.find({
        "type": {"$ne": new_item["type"]},
        "is_claimed": False
    }))

    contacted = set()
    matched_items = []

    for existing in other_items:
        prompt = f"""
Compare these two items. Are they the same lost/found item?

Item A: {existing.get('description', '')}
Item B: {new_item.get('description', '')}

Answer YES or NO.
"""
        try:
            response = gemini_model.generate_content(prompt)
            decision = (response.text or "").strip().lower()
        except Exception as e:
            logger.error(f"Gemini error: {e}")
            continue

        if decision == "yes" and existing.get("contact_info") not in contacted:
            ai_agent_notify(existing, new_item)
            contacted.add(existing.get("contact_info"))
            matched_items.append(existing)
            break  # remove break if multiple matches needed

    return matched_items

# ------------------ Matching Pipeline ------------------
def run_matching_pipeline(item_id: str) -> dict:
    """Run the full matching pipeline: TF-IDF -> Gemini -> notifications."""
    logger.info(f"🚀 Running AI matching for item {item_id}")
    item = items_col.find_one({"_id": ObjectId(item_id)})
    if not item:
        logger.warning(f"Item {item_id} not found")
        return {"action": "item_not_found"}

    # Step 1: TF-IDF
    tfidf_matches = match_with_tfidf(item)
    if tfidf_matches:
        logger.info("✅ TF-IDF matched. Skipping Gemini.")
        return {"method": "tfidf", "matches": tfidf_matches}

    # Step 2: Gemini (priority items)
    if item.get("priority"):
        gemini_matches = match_with_gemini(item)
        return {"method": "gemini", "matches": gemini_matches}

    logger.info("❌ No matches found")
    return {"method": "none", "matches": []}
