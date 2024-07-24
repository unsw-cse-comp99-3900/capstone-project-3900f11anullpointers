"""Module for sendig emails.

This module provides functionality to send emails with consent forms as a PDF to the
clinic emailand also allows sending of a confirmation email to the patient's email.

Functions:
- send_email_to_clinic: 
    Sends an email to the clinic with the consent form attached as a PDF.
- send_email_to_patient: 
    Sends a confirmation email to the patient after they submit the consent form.

Private Functions:
- _send_email: 
    Handles the actual sending of an email using the SMTP protocol with proper error handling.

Constants:
- PATIENT_SUBJECT: str
    Subject line for the confirmation email sent to the patient.

Exception Handling:
- Various smtplib.SMTP exceptions are caught to provide detailed error logging.
"""
import smtplib
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64
from datetime import datetime
import logging

PATIENT_SUBJECT: str = "Confirmation of Consent Form Submission - UNSW Optometry Clinic"

def send_email_to_clinic(server: str, port: int, email_from: str, email_to: str,
                pswd: str, attach_name: str, pdf_base64: str,
                patient_name: str, patient_email: str, submit_datetime: datetime) -> None:
    """
    Sends an email to the clinic with the consent form attached as a PDF.

    Args:
    - server (str): The SMTP server address.
    - port (int): The SMTP server port.
    - email_from (str): The sender's email address.
    - email_to (str): The recipient's email address.
    - pswd (str): The sender's email password.
    - attach_name (str): The name for the attached PDF file.
    - pdf_base64 (str): The base64-encoded content of the PDF.
    - patient_name (str): The name of the patient.
    - patient_email (str): The email address of the patient.
    - submit_datetime (datetime): The date and time the form was submitted.
    """
    subject: str = "Patient Consent Form Submission"
    current_time: str = submit_datetime.strftime("%H:%M %p")
    current_date: str = submit_datetime.strftime("%B %d, %Y")

    body: str = f"""\
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
                    <li style="color: black !important;">
                        <strong>Patient Name:</strong> {patient_name}
                    </li>
                    <li style="color: black !important;">
                        <strong>Patient Email:</strong> {patient_email}
                    </li>
                    <li style="color: black !important;">
                        <strong>Submission Date:</strong> {current_date}
                    </li>
                    <li style="color: black !important;">
                        <strong>Submission Time:</strong> {current_time}
                    </li>
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

    msg: MIMEMultipart = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = email_to
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    attachment_decoded: bytes = base64.b64decode(pdf_base64)

    attachment_package: MIMEBase = MIMEBase("application", "pdf")
    attachment_package.set_payload(attachment_decoded)
    encoders.encode_base64(attachment_package)
    attachment_package.add_header("Content-Disposition", f"attachment; filename= {attach_name}")
    msg.attach(attachment_package)

    text: str = msg.as_string()

    _send_email(server, port, email_from, email_to, pswd, text)

def send_email_to_patient(server: str, port: int, email_from: str, email_to: str,
                          pswd: str, patient_name: str) -> None:
    """
    Sends a confirmation email to the patient after they submit the consent form.

    Args:
    - server (str): The SMTP server address.
    - port (int): The SMTP server port.
    - email_from (str): The sender's email address.
    - email_to (str): The recipient's email address.
    - pswd (str): The sender's email password.
    - patient_name (str): The name of the patient.
    """
    body: str = f"""\
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

    msg: MIMEMultipart = MIMEMultipart()
    msg["From"] = email_from
    msg["To"] = email_to
    msg["Subject"] = PATIENT_SUBJECT

    msg.attach(MIMEText(body, "html"))

    text: str = msg.as_string()

    _send_email(server, port, email_from, email_to, pswd, text)

def _send_email(server: str, port: str, email_from: str,
                email_to: str, pswd: str, text: str) -> None:
    """Handles the actual sending of an email using the SMTP protocol with error handling."""
    try:
        mail_server: SMTP = SMTP(server, port)
        mail_server.starttls()
        mail_server.login(email_from, pswd)

        mail_server.sendmail(email_from, email_to, text)
        print(f"Email successfully sent to - {email_to}")
    except smtplib.SMTPAuthenticationError as e:
        logging.error("Failed to authenticate with the mail server: %s", e)
    except smtplib.SMTPConnectError as e:
        logging.error("Failed to connect to the mail server: %s", e)
    except smtplib.SMTPHeloError as e:
        logging.error("Server didn't reply properly to the HELO greeting: %s", e)
    except smtplib.SMTPSenderRefused as e:
        logging.error("Sender address was refused by the server: %s", e)
    except smtplib.SMTPRecipientsRefused as e:
        logging.error("Recipient address was refused by the server: %s", e)
    except smtplib.SMTPDataError as e:
        logging.error("The server replied with an unexpected error code: %s", e)
    except smtplib.SMTPNotSupportedError as e:
        logging.error("The command or option is not supported by the server: %s", e)
    except smtplib.SMTPServerDisconnected as e:
        logging.error("Server unexpectedly disconnected: %s", e)
    except smtplib.SMTPException as e:
        logging.error("An error occurred while sending the email: %s", e)
    finally:
        mail_server.quit()
