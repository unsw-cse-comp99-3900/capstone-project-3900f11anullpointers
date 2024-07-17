import shutil
import secrets
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.pdf_gen import GeneratePDF
import os
import logging
import time

import re
from src.send_email import send_clinic_email, send_patient_email

TEMP_PDF_DIR = "/temp_pdfs"
os.makedirs(TEMP_PDF_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# Docker directory where PDFs are stored
# PDF_DIR = '/app/pdfs'
PDF_DIR = ""
SERVER = "smtp.gmail.com"
PORT = 587
EMAIL_FROM = "anullpointers@gmail.com"
CLINIC_EMAIL = "nicholas.abreu@outlook.com"
PSWD = "rtrjqzvtyuecbyxh"

################### Helper Functions ###################
# Function to set up email to be sent.
def _send_email_to_clinic(pdf_path: str, patient_name: str) -> None:
    with open(pdf_path, 'rb') as attachment:
        send_clinic_email(
            SERVER,
            PORT,
            EMAIL_FROM,
            CLINIC_EMAIL,
            PSWD,
            patient_name,
            os.path.basename(pdf_path),
            attachment
        )

def _send_email_to_patient(email: str, patient_name: str) -> None:
    send_patient_email(SERVER, PORT, EMAIL_FROM, email, PSWD, patient_name)

# Function to validate user data.
def validateData(received_data):
    # Check for required fields and empty values.
    required_fields = ['name', 'email', 'signature', 'consent']
    for field in required_fields:
        # If any field other than 'consent' is empty, return error.
        if field not in received_data or received_data[field] == "":
            return jsonify({"error": f"Field '{field}' is required and cannot be empty."}), 400

    # Validate email format.
    email = received_data['email']
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_regex, email):
        return jsonify({"error": "Invalid email format."}), 400
    
    # Validate consent field.
    consent = received_data['consent']
    if not isinstance(consent, dict) or 'researchConsent' not in consent or 'studentConsent' not in consent:
        return jsonify({"error": "Consent fields are invalid."}), 400
    
    # Check if consent fields are boolean.
    if not isinstance(consent['researchConsent'], bool) or not isinstance(consent['studentConsent'], bool):
        return jsonify({"error": "Consent fields must be boolean values."}), 400
    
    # Return success response if all validations pass.
    return jsonify({"message": "Validation successful."}), 200

    # Validate phone number format and length.
    # phone_number = received_data['phone']
    # if not (phone_number.isdigit() and len(phone_number) == 10):
    #     return jsonify({"error": "Phone number must be a 10-digit numeric value."}), 400

    # Validate date of birth format and values.
    # dob = received_data['dob']
    # if not (len(dob) == 10 and dob[4] == dob[7] == '-' and dob[:4].isdigit() and dob[5:7].isdigit() and dob[8:].isdigit()):
    #     return jsonify({"error": "Invalid date of birth format. Use DD-MM-YYYY."}), 400

    # yyyy, mm, dd = map(int, dob.split('-'))
    # if not (0 < dd <= 31 and 0 < mm <= 12):
    #     return jsonify({"error": "Invalid date of birth values. Check day, month, and year."}), 400
########################################################

@app.route('/post', methods=['POST'])
def post_method():
    try:
        received_data = request.json
        validateData(received_data)

        # Determine consent flags based on consent field
        consent = received_data.get('consent')
        consent_flags = [consent['researchConsent'], False, False]

        # Generate 4 byte token with name prepended, removing unnecessary special characters
        token = re.sub(r"[^a-zA-Z' -]", "", received_data['name']).replace(" ", "_") + " - " + secrets.token_hex(4)

        # Generate PDF with dynamic data
        generator = GeneratePDF()
        pdf_path = os.path.join(PDF_DIR, f"{token}.pdf")
        generator.generate_pdf(token, received_data['name'], "adult", consent_flags)

        # Send email of PDF
        email_sent = send_email_with_pdf(pdf_path, "z5361148@ad.unsw.edu.au")
        
        if not email_sent:
            # Move the PDF to the temporary storage directory if the email fails to send
            temp_pdf_path = os.path.join(TEMP_PDF_DIR, f"{very_special_name}.pdf")
            shutil.move(pdf_path, temp_pdf_path)
            logging.error(f"PDF moved to temporary storage: {temp_pdf_path}")
        else:
            # Delete the generated PDF file from the server if the email was sent successfully
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
        # Send email of PDF to clinic
        _send_email_to_clinic(pdf_path, received_data['name'])
        # Send confirmation email to patient
        _send_email_to_patient(received_data["email"], received_data['name'])

        # Delete the generated PDF file from the server
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

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