import requests
import os

EMAILJS_SERVICE_ID = os.getenv("EMAILJS_SERVICE_ID")
EMAILJS_TEMPLATE_ID = os.getenv("EMAILJS_TEMPLATE_ID")
EMAILJS_PUBLIC_KEY = os.getenv("EMAILJS_PUBLIC_KEY")

def send_code(email, code):
    """Send SBVM code via EmailJS REST API"""
    url = "https://api.emailjs.com/api/v1.0/email/send"
    payload = {
        "service_id": EMAILJS_SERVICE_ID,
        "template_id": EMAILJS_TEMPLATE_ID,
        "user_id": EMAILJS_PUBLIC_KEY,
        "template_params": {
            "to_email": email,
            "secure_code": code
        }
    }
    try:
        r = requests.post(url, json=payload, timeout=5)
        if r.status_code == 200:
            print(f"[EmailJS] Code sent successfully to {email}")
        else:
            print(f"[EmailJS] Failed to send code to {email}: {r.text}")
    except Exception as e:
        print(f"[EmailJS] Error: {e}")
