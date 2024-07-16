import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import base64
from io import BytesIO
from datetime import datetime   
import logging

def send_emails(server: str, port: int, email_from: str, email_to: str, 
                pswd :str, attach_name:str , pdf_base64: str, 
                patient_name: str, patient_email: str, submit_datetime: datetime) -> None:
    subject = "Patient Consent Form Submission"
    patient_name = patient_name
    patient_email = patient_email
    
    current_time = submit_datetime.strftime("%H:%M %p")
    current_date = submit_datetime.strftime("%B %d, %Y")
    
    body = f"""\
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Patient Consent Form Submission</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #dddddd; border-radius: 5px; background-color: #ffffff;">
            <div style="text-align: center; border-bottom: 1px solid #dddddd; padding-bottom: 20px;">
                <h1 style="margin: 0; color: black !important;">Patient Consent Form Submission</h1>
            </div>

            <div style="padding: 20px color: black !important;">
                <h2 style="margin-top: 0 color: black !important;">New Consent Form Received</h2>
                <p style="color: black !important;">A new patient consent form has been submitted with the following details:</p>
                <ul>
                    <li style="color: black !important;"><strong>Patient Name:</strong> {patient_name}</li>
                    <li style="color: black !important;"><strong>Patient Email:</strong> {patient_email}</li>
                    <li style="color: black !important;"><strong>Submission Date:</strong> {current_date}</li>
                    <li style="color: black !important;"><strong>Submission Time:</strong> {current_time}</li>
                </ul>
                <p style="color: black !important;">The completed consent form is attached to this email as a PDF file.</p>
                <p style="color: black !important;">Please process this form according to our standard procedures and add it to the patient's records.</p>
                <p style="color: black !important;">If you notice any issues with the form or require additional information, please contact the patient directly.</p>
            </div>

            <div style="text-align: center; border-top: 1px solid #dddddd; padding-top: 20px; font-size: 12px; color: #888888;">
                <p>This is an automated message from our patient consent form system.</p>
                <p>If you have any questions, please contact the IT department.</p>
                <p>&copy; 2024 Your Clinic Name. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """    
    
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))
    
    attachment_decoded = base64.b64decode(pdf_base64)
    
    attachment_package = MIMEBase('application', 'pdf')
    attachment_package.set_payload(attachment_decoded)
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', f"attachment; filename= {attach_name}")
    msg.attach(attachment_package)

    text = msg.as_string()

    try:
        TIE_server = smtplib.SMTP(server, port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)

        TIE_server.sendmail(email_from, email_to, text)
        print(f"Email successfully sent to - {email_to}")
    except Exception as e:
        logging.error(e)
    finally:
        TIE_server.quit()