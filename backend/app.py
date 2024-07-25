import shutil
import secrets
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.pdf_gen import GeneratePDF
from src.send_email import send_email_to_clinic, send_email_to_patient
import os
import logging
import time

import re
from src.send_email import send_clinic_email, send_patient_email
from dotenv import find_dotenv, load_dotenv 
from datetime import datetime
import pytz

load_dotenv(find_dotenv('.env'))
load_dotenv(find_dotenv('.env.local'))

FRONTEND_HOST = os.getenv('NEXT_PUBLIC_HOST')
FRONTEND_PORT = os.getenv('NEXT_PUBLIC_FRONTEND_PORT')
FRONTEND_URL = f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"

TEMP_PDF_DIR = "/temp_pdfs"
os.makedirs(TEMP_PDF_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": FRONTEND_URL}})

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# Docker directory where PDFs are stored
# PDF_DIR = '/app/pdfs'
PDF_DIR = ""

# Function to set up email to be sent to clinic and patient
def send_emails(recipient_email, pdf_base64, patient_name, patient_email, submit_datetime):
    server = os.getenv('SMTP_HOST')
    port = os.getenv('SMTP_PORT')
    email_from = os.getenv('SMTP_USER')
    email_to = recipient_email
    pswd = os.getenv('SMTP_PSWD')

    token = re.sub(r"[^a-zA-Z' -]", "", patient_name).replace(" ", "_") + " - " + secrets.token_hex(4)

    send_email_to_clinic(server, port, email_from, email_to, pswd, f"{token}.pdf",
                pdf_base64, patient_name, patient_email, submit_datetime)

    send_email_to_patient(server, port, email_from, patient_email, pswd, patient_name)

@app.route('/post', methods=['POST'])
def post_method():
    try:
        received_data = request.json

        logging.info(received_data)

        au_timezone = pytz.timezone('Australia/Sydney')
        current_au_time = datetime.now(au_timezone)

        draw_signature = received_data.get('drawSignature')
        form_type = received_data.get('formType')
        generator = GeneratePDF()

        # Determine consent flags based on consent field
        consent = received_data.get('consent')

        if form_type == "adult":
            consent_flags = [consent['researchConsent'], consent['contactConsent'], consent['studentConsent']]
        elif form_type == "child":
            consent_flags = [consent['researchConsent'], consent['studentConsent']]
        else:
            raise FileNotFoundError(f"Form type is not available: {form_type}")

        # Generate PDF with dynamic data
        pdf_base64 = generator.generate_pdf(
            received_data['name'],
            form_type,
            consent_flags,
            draw_signature,
            current_au_time
        )

        patient_name = received_data.get('name')
        patient_email = received_data.get('email')

        send_emails(os.getenv('RECIPIENT_EMAIL'), pdf_base64,
                    patient_name, patient_email, current_au_time)

        response_data = {
            "message": "Form submission successful",
            "received_data": received_data,
        }

        return jsonify(response_data), 200

    except Exception as e:
        logging.error(e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3030, threaded=True)
