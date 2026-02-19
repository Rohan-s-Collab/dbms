# backend/notif.py
from dotenv import load_dotenv
import os
import logging
from email.message import EmailMessage
import smtplib
from twilio.rest import Client

# Load env (redundant safety — okay to keep)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Logging setup
logger = logging.getLogger("notif")
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Email config
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASS")

# Twilio config
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

# Debug log — show which credentials loaded
logger.info("🔍 Twilio SID: %s", "Loaded ✅" if TWILIO_ACCOUNT_SID else "Missing ❌")
logger.info("🔍 Twilio Token: %s", "Loaded ✅" if TWILIO_AUTH_TOKEN else "Missing ❌")
logger.info("🔍 Twilio Phone: %s", TWILIO_PHONE or "Missing ❌")

# ------------------ Send Email ------------------
def send_email(to: str, subject: str, body: str) -> None:
    if not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        logger.warning("❌ Email credentials not set; skipping email to %s", to)
        return
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to
        msg.set_content(body)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        logger.info("✅ Email sent to %s", to)
    except Exception:
        logger.exception("❌ Failed to send email to %s", to)

# ------------------ Twilio Call ------------------
def make_phone_call(to_number: str, message: str) -> None:
    if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE):
        logger.warning("⚠️ Twilio credentials missing; skipping call to %s", to_number)
        return
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        call = client.calls.create(
            twiml=f'<Response><Say>{message}</Say></Response>',
            to=to_number,
            from_=TWILIO_PHONE
        )
        logger.info("📞 Call initiated to %s sid=%s", to_number, call.sid)
    except Exception:
        logger.exception("❌ Twilio call failed for %s", to_number)
