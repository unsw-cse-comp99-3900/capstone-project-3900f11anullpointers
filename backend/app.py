import os
import logging
import secrets
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.pdf_gen import GeneratePDF
from src.send_email import send_clinic_email, send_patient_email

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# Docker directory where PDFs are stored
PDF_DIR = ""
SERVER = "smtp.gmail.com"
PORT = 587
EMAIL_FROM = "anullpointers@gmail.com"
CLINIC_EMAIL = "nicholas.abreu@outlook.com"
PSWD = "rtrjqzvtyuecbyxh"

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

@app.route('/post', methods=['POST'])
def post_method():
    try:
        received_data = request.json

        logging.info(received_data)

        # Determine consent flags based on consent field
        consent = received_data.get('consent')
        consent_flags = [consent['researchConsent'], False, False]

        # Generate 16 byte token
        token = secrets.token_hex(16)

        # Generate PDF with dynamic data
        generator = GeneratePDF()
        pdf_path = os.path.join(PDF_DIR, f"{token}.pdf")
        generator.generate_pdf(token, received_data['name'], "adult", consent_flags)

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