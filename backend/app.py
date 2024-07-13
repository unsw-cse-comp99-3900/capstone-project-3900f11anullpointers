from flask import Flask, request, jsonify
from flask_cors import CORS
from src.pdf_gen import GeneratePDF
from src.send_email import send_emails
import os
import logging
from dotenv import find_dotenv, load_dotenv 

load_dotenv(find_dotenv('.env'))
load_dotenv(find_dotenv('.env.local'))

FRONTEND_HOST = os.getenv('NEXT_PUBLIC_HOST')
FRONTEND_PORT = os.getenv('NEXT_PUBLIC_FRONTEND_PORT')
FRONTEND_URL = f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": FRONTEND_URL}})

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

# Docker directory where PDFs are stored
# PDF_DIR = '/app/pdfs'
PDF_DIR = ""

# Function to set up email to be sent.
def send_email_with_pdf(pdf_path, recipient_email):
    SERVER = os.getenv('SMTP_HOST')
    PORT = os.getenv('SMTP_PORT')
    EMAIL_FROM = os.getenv('SMTP_USER')
    EMAIL_TO = recipient_email
    PSWD = os.getenv('SMTP_PSWD')

    with open(pdf_path, 'rb') as attachment:
        send_emails(SERVER, PORT, EMAIL_FROM, EMAIL_TO, PSWD, "Consent Form.pdf", attachment)

@app.route('/post', methods=['POST'])
def post_method():
    try:
        received_data = request.json

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
        #send_email_with_pdf(pdf_path, os.getenv('RECIPIENT_EMAIL'))

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