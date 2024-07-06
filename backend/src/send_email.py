import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

def send_emails(server, port, email_from, email_to, pswd, attachment_name, attachment):
    subject = "Patient consent form"
    name = "[Recipient's Name]"
    address = "[Recipient's Address]"
    phone_number = "[Recipient's Phone Number]"
    dob = "[Recipient's Date of Birth]"
    signature = "[Recipient's Signature]"
    
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
            <h2 style="margin-top: 0">Dear {name},</h2>
            <p>
            Thank you for filling out the confirmation form. Here are the details
            you provided:
            </p>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Address:</strong> {address}</p>
            <p><strong>Phone Number:</strong> {phone_number}</p>
            <p><strong>Date of Birth:</strong> {dob}</p>
            <p><strong>Signature:</strong> {signature}</p>
            <p>
            If any of the information above is incorrect, please contact us
            immediately.
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
    
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'html'))
    
    attachment_package = MIMEBase('application', 'octet-stream')
    attachment_package.set_payload((attachment).read())
    encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= " + attachment_name)
    msg.attach(attachment_package)
    
    text = msg.as_string()
    
    try:
        TIE_server = smtplib.SMTP(server, port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)

        TIE_server.sendmail(email_from, email_to, text)
        print(f"Email successfully sent to - {email_to}")
    except Exception as e:
        print(e)
    finally:
        TIE_server.quit()