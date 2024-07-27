import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import base64
from datetime import datetime   
import logging
import threading
import time

class SendEmail:
    def __init__(self, server, port, user, pswd):
        self.server = server
        self.port = port
        self.user = user
        self.pswd = pswd
            
    def start(self) -> smtplib.SMTP:
        try:
            connection = smtplib.SMTP(self.server, self.port)
            connection.starttls()
            connection.login(self.user, self.pswd)
        except Exception as e:
            logging.error(e)
        
        return connection
    
    def close(self, connection) -> None:
        connection.close()
    
    def send_email(self, connection, email_to, subject, body, attach_name="Consent Form.pdf", pdf_base64=None):
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = email_to
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'html'))

        if pdf_base64 != None:
            attachment_decoded = base64.b64decode(pdf_base64)
            attachment_package = MIMEBase('application', 'pdf')
            attachment_package.set_payload(attachment_decoded)
            encoders.encode_base64(attachment_package)
            attachment_package.add_header('Content-Disposition', f"attachment; filename= {attach_name}")
            msg.attach(attachment_package)

        text = msg.as_string()
        connection.sendmail(self.user, email_to, text)
            
    def send_email_to_clinic(self, connection, email_to: str, attach_name:str , pdf_base64: str,
                    patient_name: str, patient_email: str, submit_datetime: datetime) -> None:
        subject = "Patient Consent Form Submission"
        current_time = submit_datetime.strftime("%l:%M %p")
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
        
        try:
            self.send_email(connection, email_to, subject, body, attach_name=attach_name, pdf_base64=pdf_base64)
        except Exception as e:
            logging.error(e)
            

    def send_email_to_patient(self, connection, email_to: str, patient_name: str) -> None:
        subject = "Confirmation of Consent Form Submission - UNSW Optometry Clinic"

        body = f"""\
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Confirmation Email</title>
        </head>
        <body
            style="
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            "
        >
            <div
            style="
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #dddddd;
                border-radius: 5px;
                background-color: #ffffff;
            "
            >
            <div
                style="
                text-align: center;
                border-bottom: 1px solid #dddddd;
                padding-bottom: 20px;
                "
            >
                <h1 style="margin: 0; color: black">Confirmation Email</h1>
            </div>

            <div style="padding: 20px; color: black">
                <h2 style="margin-top: 0">Dear {patient_name},</h2>
                <p>
                Thanks for filling out the consent form for the UNSW Optometry Clinic.
                We appreciate your time and effort in providing us with your information and consent.
                </p>

                <p>
                Thank you for choosing UNSW Optometry Clinic.
                </p>
            </div>

            <div
                style="
                text-align: center;
                border-top: 1px solid #dddddd;
                padding-top: 20px;
                font-size: 12px;
                color: #888888;
                "
            >
                <p>This is an automated message, please do not reply.</p>
                <p>&copy; 2024 Your Company. All rights reserved.</p>
            </div>
            </div>
        </body>
        </html>
        """
        
        try:
            self.send_email(connection, email_to, subject, body)
        except Exception as e:
            logging.error(e)