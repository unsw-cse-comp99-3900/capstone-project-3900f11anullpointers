from flask import Flask, request, jsonify
from flask_cors import CORS
from src.pdf_gen import GeneratePDF
from src.send_email import send_emails
import os
import logging
import re

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# Docker directory where PDFs are stored
# PDF_DIR = '/app/pdfs'
PDF_DIR = ""

################### Helper Functions ###################
# Function to set up email to be sent.
def send_email_with_pdf(pdf_path, recipient_email):
    SERVER = "smtp.gmail.com"
    PORT = 587
    EMAIL_FROM = "anullpointers@gmail.com"
    EMAIL_TO = recipient_email
    PSWD = "rtrjqzvtyuecbyxh"

    with open(pdf_path, 'rb') as attachment:
        send_emails(SERVER, PORT, EMAIL_FROM, EMAIL_TO, PSWD, os.path.basename(pdf_path), attachment)

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
        logging.info(received_data)

        # Determine consent flags based on consent field
        consent = received_data.get('consent')
        consent_flags = [consent['researchConsent'], False, False]

        very_special_name = "test1"

        # Generate PDF with dynamic data
        generator = GeneratePDF()
        pdf_path = os.path.join(PDF_DIR, f"{very_special_name}.pdf")
        generator.generate_pdf(very_special_name, received_data['name'], "adult", consent_flags)

        # Send email of PDF
        send_email_with_pdf(pdf_path, "engin.k1@outlook.com")

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
    app.run(debug=True, host='0.0.0.0', port=3030)