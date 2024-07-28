"""Flask web app to handle pdf and email generation.

This module handles the PDF generation and email sending for form submissions 
through a Flask web application. The app listens for POST requests and processes 
the received data to generate a PDF and send emails to specified recipients.

Functions:
- post_method: Endpoint for handling form submissions.

Private Functions:
- send_emails: Sends emails with the generated PDF attached.
"""

import os
import logging
import secrets
import re
from typing import Any, Dict, List
from datetime import datetime
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from src.pdf_gen import GeneratePDF
from src.send_email import send_email_to_clinic, send_email_to_patient
from dotenv import find_dotenv, load_dotenv
import pytz

load_dotenv(find_dotenv(".env"))
load_dotenv(find_dotenv(".env.local"))

FRONTEND_HOST = os.getenv("NEXT_PUBLIC_HOST")
FRONTEND_PORT = os.getenv("NEXT_PUBLIC_FRONTEND_PORT")
FRONTEND_URL = f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": FRONTEND_URL}})

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

def _send_emails(recipient_email: str, pdf_base64, patient_name: str,
                patient_email: str, submit_datetime: datetime) -> None:
    """Sends emails with the generated PDF attached."""
    server: str = os.getenv("SMTP_HOST")
    port: str = os.getenv("SMTP_PORT")
    email_from: str = os.getenv("SMTP_USER")
    email_to: str = recipient_email
    pswd: str = os.getenv("SMTP_PSWD")

    reg_name: str = re.sub(r"[^a-zA-Z' -]", "", patient_name).replace(" ", "_")
    token: str = reg_name + " - " + secrets.token_hex(4)

    send_email_to_clinic(server, port, email_from, email_to, pswd, f"{token}.pdf",
                pdf_base64, patient_name, patient_email, submit_datetime)

    send_email_to_patient(server, port, email_from, patient_email, pswd, patient_name)

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

        logging.info(received_data)

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
