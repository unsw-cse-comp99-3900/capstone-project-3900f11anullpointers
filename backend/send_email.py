import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_emails(server, port, email_from, email_to, pswd, attachment_name, attachment):
    subject = "Patient consent form"
    
    body = """
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Confirmation Email</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 200px;
                padding: 0;
            }
            .email-container {
                background-color: #ffffff;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #dddddd;
                border-radius: 5px;
            }
            .header {
                text-align: center;
                padding-bottom: 20px;
                border-bottom: 1px solid #dddddd;
            }
            .content {
                padding: 20px 0;
            }
            .content h2 {
                margin-top: 0;
            }
            .content p {
                margin: 10px 0;
            }
            .footer {
                text-align: center;
                padding-top: 20px;
                border-top: 1px solid #dddddd;
                font-size: 12px;
                color: #888888;
            }
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>Confirmation Email</h1>
            </div>
            <div class="content">
                <h2>Dear [Recipient's Name],</h2>
                <p>Thank you for filling out the confirmation form. Here are the details you provided:</p>
                <p><strong>Name:</strong> [Recipient's Name]</p>
                <p><strong>Address:</strong> [Recipient's Address]</p>
                <p><strong>Phone Number:</strong> [Recipient's Phone Number]</p>
                <p><strong>Date of Birth:</strong> [Recipient's Date of Birth]</p>
                <p><strong>Consent Received:</strong> [Yes/No]</p>
                <p><strong>Signature:</strong> [Recipient's Signature]</p>
                <p>If any of the information above is incorrect, please contact us immediately.</p>
            </div>
            <div class="footer">
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

SERVER = "smtp.gmail.com"
PORT = 587

EMAIL_FROM = "darren19032@gmail.com"
EMAIL_TO = "darren.nguyen1903@gmail.com"

PSWD = "inxdxpynmzyqohtz"

FILENAME = "test1.pdf"
DIRECTORY = f"backend/{FILENAME}"
attachment = open(DIRECTORY, 'rb')

send_emails(SERVER, PORT, EMAIL_FROM, EMAIL_TO, PSWD, FILENAME, attachment)