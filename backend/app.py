import os
import logging
import secrets
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.pdf_gen import GeneratePDF
from src.send_email import SendEmail
import os
import logging
from dotenv import find_dotenv, load_dotenv 
from datetime import datetime
import pytz
import time
import threading


load_dotenv(find_dotenv('.env'))
load_dotenv(find_dotenv('.env.local'))

FRONTEND_HOST = os.getenv('NEXT_PUBLIC_HOST')
FRONTEND_PORT = os.getenv('NEXT_PUBLIC_FRONTEND_PORT')
FRONTEND_URL = f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": FRONTEND_URL}})

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

server = os.getenv('SMTP_HOST')
port = os.getenv('SMTP_PORT')
user = os.getenv('SMTP_USER')
pswd = os.getenv('SMTP_PSWD')
smtp_server = SendEmail(server, port, user, pswd)

def send_email_clinic(email_to, pdf_base64, patient_name, patient_email, submit_datetime):
    token = re.sub(r"[^a-zA-Z' -]", "", patient_name).replace(" ", "_") + " - " + secrets.token_hex(4)

    start = time.time()
    connection = smtp_server.start()
    smtp_server.send_email_to_clinic(connection, email_to, f"{token}.pdf", pdf_base64, patient_name, patient_email, submit_datetime)
    smtp_server.close(connection)
    end = time.time()
    logging.info(f"Email successfully sent to the clinic. Elapsed time: {end-start:.2f} sec")
    
def send_email_patient(patient_email, patient_name):
    start = time.time()
    connection = smtp_server.start()
    smtp_server.send_email_to_patient(connection, patient_email, patient_name)
    smtp_server.close(connection)
    end = time.time()
    logging.info(f"Email successfully sent to the patient. Elapsed time: {end-start:.2f} sec")
    
# Function to set up email to be sent to clinic and patient
def send_emails(recipient_email, pdf_base64, patient_name, patient_email, submit_datetime):  
    start = time.time()
    
    t1 = threading.Thread(target=send_email_clinic, args=(recipient_email, pdf_base64, patient_name, patient_email, submit_datetime))
    t2 = threading.Thread(target=send_email_patient, args=(patient_email, patient_name))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    
    end = time.time()
    logging.info(f"Emails sent successfully. Total elapsed time: {end-start:.2f} sec")

@app.route('/post', methods=['POST'])
def post_method():
    try:
        received_data = request.json

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
