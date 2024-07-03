from flask import Flask, request, jsonify
from flask_cors import CORS
from src.pdf_gen import GeneratePDF
from src.send_email import send_emails
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Docker directory where PDFs are stored
PDF_DIR = ''

# Function to set up email to be sent.
def send_email_with_pdf(pdf_path, recipient_email):
    SERVER = "smtp.gmail.com"
    PORT = 587
    EMAIL_FROM = "anullpointers@gmail.com"
    EMAIL_TO = recipient_email
    PSWD = "rtrjqzvtyuecbyxh"

    with open(pdf_path, 'rb') as attachment:
        send_emails(SERVER, PORT, EMAIL_FROM, EMAIL_TO, PSWD, os.path.basename(pdf_path), attachment)

@app.route('/post', methods=['POST'])
def post_method():
    try:
        received_data = request.json

        # Check for required fields and empty values
        required_fields = ['name', 'email', 'phone', 'address', 'dob', 'consent']
        for field in required_fields:
            if field != 'consent' and (field not in received_data or not received_data[field]):
                return jsonify({"error": f"Field '{field}' is required and cannot be empty."}), 400

        # Validate email format
        email = received_data['email']
        if '@' not in email:
            return jsonify({"error": "Email must contain the '@' symbol."}), 400

        # Validate phone number format and length
        phone_number = received_data['phone']
        if not (phone_number.isdigit() and len(phone_number) == 10):
            return jsonify({"error": "Phone number must be a 10-digit numeric value."}), 400

        # Validate date of birth format and values
        dob = received_data['dob']
        if not (len(dob) == 10 and dob[4] == dob[7] == '-' and dob[:4].isdigit() and dob[5:7].isdigit() and dob[8:].isdigit()):
            return jsonify({"error": "Invalid date of birth format. Use DD-MM-YYYY."}), 400

        yyyy, mm, dd = map(int, dob.split('-'))
        if not (0 < dd <= 31 and 0 < mm <= 12):
            return jsonify({"error": "Invalid date of birth values. Check day, month, and year."}), 400

        # Determine consent flags based on consent field
        consent = received_data.get('consent', False)
        consent_flags = [consent, consent, consent]
        very_special_name = "test1"

        # Generate PDF with dynamic data
        generator = GeneratePDF()
        pdf_path = os.path.join(PDF_DIR, f"{very_special_name}.pdf")
        generator.generate_pdf(very_special_name, received_data['name'], "adult", consent_flags)

        # Send email of PDF
        send_email_with_pdf(pdf_path, "nicholas.abreu@outlook.com")

        # Delete the generated PDF file from the server
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        response_data = {
            "message": "Form submission successful",
            "received_data": received_data,
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3030)