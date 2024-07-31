"""Flask web app to handle pdf and email generation.

This module handles the PDF generation and email sending for form submissions 
through a Flask web application. The app listens for POST requests and processes 
the received data to generate a PDF and send emails to specified recipients.

Functions:
- post_method: Endpoint for handling form submissions.

Private Functions:
- send_emails: Sends emails with the generated PDF attached.
- validate_signature: Validates the base64 encoded signature image.
- validate_input: Validates all input data.
"""

import os
import logging
import secrets
import re
import base64
import io
import time
import threading
from typing import Any, Dict, List
from datetime import datetime
import pytz
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from dotenv import find_dotenv, load_dotenv
from PIL import Image
from src.pdf_gen import GeneratePDF
from src.send_email import SendEmail

load_dotenv(find_dotenv(".env"))
load_dotenv(find_dotenv(".env.local"))

FRONTEND_HOST = os.getenv("NEXT_PUBLIC_HOST")
FRONTEND_PORT = os.getenv("NEXT_PUBLIC_FRONTEND_PORT")
FRONTEND_URL = f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

server = os.getenv("SMTP_HOST")
port = os.getenv("SMTP_PORT")
user = os.getenv("SMTP_USER")
pswd = os.getenv("SMTP_PSWD")
smtp_server = SendEmail(server, port, user, pswd)

# Function to set up email to be sent to clinic and patient
def _send_emails(recipient_email, pdf_base64, patient_name, patient_email, submit_datetime):
    """Sends emails with the generated PDF attached."""

    start = time.time()

    reg_name: str = re.sub(r"[^a-zA-Z' -]", "", patient_name).replace(" ", "_")
    token: str = reg_name + "_" + secrets.token_hex(4)

    t1 = threading.Thread(
        target=smtp_server.send_email_to_clinic,
        args=(
            recipient_email,
            f"{token}.pdf",
            pdf_base64,
            patient_name,
            patient_email,
            submit_datetime
        )
    )
    t2 = threading.Thread(
        target=smtp_server.send_email_to_patient,
        args=(patient_email, patient_name)
    )

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    end = time.time()
    logging.info("Emails sent successfully. Total elapsed time: %.2f sec", end - start)

def validate_signature(signature_base64: str) -> None:
    """Validates the base64 encoded signature image."""
    try:
        # Decode the base64 string
        signature_base64: str = signature_base64.split("base64,")[1]
        signature_data = base64.b64decode(signature_base64)
        
        # Open the image
        image = Image.open(io.BytesIO(signature_data))
        # Validate image format
        if image.format != 'PNG':
            raise ValueError("Signature image must be in PNG format")

        # Validate image dimensions
        if image.width > 1200 or image.height > 200:
            raise ValueError("Signature image dimensions are invalid")

    except Exception as e:
        raise ValueError("Invalid signature image: " + str(e))    

def validate_input(data: Dict[str, Any]) -> None:
    """Validates the input data."""
    if not isinstance(data.get("name"), str) or not data["name"].strip():
        raise ValueError("Invalid name")

    email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not isinstance(data.get("email"), str) or not re.match(email_pattern, data["email"]):
        raise ValueError("Invalid email")

    base64_png_pattern = r"^data:image/png(?:;charset=utf-8)?;base64,[A-Za-z0-9+/=]+$"
    if not isinstance(data.get("drawSignature"), str) or not data["drawSignature"].strip():
        raise ValueError("Invalid drawSignature")
    
    if not re.match(base64_png_pattern, data["drawSignature"]):
        raise ValueError("Invalid drawSignature: Not a valid Base64 PNG data URI.")

    # Validate base64 signature image
    validate_signature(data["drawSignature"])

    if data.get("formType") not in ["adult", "child"]:
        raise ValueError("Invalid formType")

    consent = data.get("consent")
    if not isinstance(consent, dict):
        raise ValueError("Invalid consent data")
    
    if data["formType"] == "child":
        required_consent_keys = {"researchConsent", "studentConsent"}
        if "contactConsent" in consent:
            del consent["contactConsent"]
    elif data["formType"] == "adult":
        required_consent_keys = {"researchConsent", "contactConsent", "studentConsent"}

    if required_consent_keys != set(consent.keys()):
        raise ValueError("Missing or extra consent fields")

    for key in required_consent_keys:
        if not isinstance(consent[key], bool):
            raise ValueError(f"Invalid value for {key}")    

@app.route("/post", methods=["POST"])
def post_method() -> Response:
    """
    Endpoint for handling form submissions.

    This endpoint accepts a JSON payload, generates a PDF from the received data, 
    and sends emails to the clinic and the patient. It returns a success message 
    and the received data upon successful processing.

    Returns:
        Response: JSON response with a success message and the received data or 
                  an error message in case of failure.
    """
    try:
        received_data: Dict[str, Any] = request.json


        validate_input(received_data)

        current_au_time: datetime = datetime.now(pytz.timezone("Australia/Sydney"))

        draw_signature: str = received_data.get("drawSignature")
        form_type: str = received_data.get("formType")
        generator: GeneratePDF = GeneratePDF()

        # Determine consent flags based on consent field
        consent: Dict[str, bool] = received_data.get("consent")

        if form_type == "adult":
            consent_flags: List[bool] = [
                consent["researchConsent"],
                consent["contactConsent"],
                consent["studentConsent"],
            ]
        elif form_type == "child":
            consent_flags: List[bool] = [consent["researchConsent"], consent["studentConsent"]]
        else:
            raise FileNotFoundError(f"Form type is not available: {form_type}")

        # Generate PDF with dynamic data
        pdf_base64: str = generator.generate_pdf(
            received_data["name"],
            form_type,
            consent_flags,
            draw_signature,
            current_au_time
        )

        patient_name: str = received_data.get("name")
        patient_email: str = received_data.get("email")

        _send_emails(os.getenv("RECIPIENT_EMAIL"), pdf_base64,
                    patient_name, patient_email, current_au_time)

        response_data: Dict[str, Any] = {
            "message": "Form submission successful",
            "received_data": received_data,
        }

        return jsonify(response_data), 200

    except Exception as e:
        logging.error(e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3030, threaded=True)
