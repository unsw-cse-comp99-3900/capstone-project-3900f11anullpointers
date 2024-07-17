import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

CLINIC_EMAIL_SUBJECT = "Patient consent form"
CLINIC_NAME = "UNSW Optometry Clinic"

PATIENT_EMAIL_SUBJECT = "Confirmation of Consent Form Submission - UNSW Optometry Clinic"

def send_clinic_email(server, port, email_from, email_to, pswd, patient_name, attachment_name, attachment):
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
            <h2 style="margin-top: 0">Dear {CLINIC_NAME},</h2>
            <p>
            {patient_name} has filled out the consent form. Please find the attached consent form.
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
    msg['Subject'] = CLINIC_EMAIL_SUBJECT

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

def send_patient_email(server, port, email_from, email_to, pswd, patient_name):
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

    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = PATIENT_EMAIL_SUBJECT

    msg.attach(MIMEText(body, 'html'))
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

def email_test():
    server = "smtp.gmail.com"
    port = 587

    email_from = "anullpointers@gmail.com"
    email_to = "z5425707@ad.unsw.edu.au"
    patient_name = "Trevor"

    # app password
    pswd = "rtrjqzvtyuecbyxh"

    filename = "test1.pdf"
    attachment = open(filename, 'rb')

    send_clinic_email(server, port, email_from, email_to, pswd, patient_name, filename, attachment)

if __name__ == '__main__':
    email_test()
