import unittest
from unittest.mock import patch, MagicMock, ANY
import smtplib, base64
from datetime import datetime
from src.send_email import send_email_to_clinic,  send_email_to_patient

class TestSendClinicEmails(unittest.TestCase):
    def setUp(self) -> None:
        self.server = "smtp.gmail.com"
        self.port = 587
        self.email_from = "anullpointers@gmail.com"
        self.email_to = "z5361148@ad.unsw.edu.au"
        self.pswd = "jrowigmvzvtoifhz"
        self.attachment_name = "bobs_consent_info.pdf"
        self.attachment_content = base64.b64encode(b'pdf content').decode('utf-8')
        self.patient_name = 'Bob Marley'
        self.patient_email = "z5361148@ad.unsw.edu.au"
        self.datetime = datetime.now()
        
    @patch('smtplib.SMTP')
    def test_send_clinic_email_success(self, mock_smtp):
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Call the send_emails function
        send_email_to_clinic(self.server, self.port, self.email_from, self.email_to, 
                             self.pswd, self.attachment_name, self.attachment_content,
                             self.patient_name, self.patient_email, self.datetime)

        # Assertions to check if email sending process is called correctly
        mock_smtp.assert_called_with(self.server, self.port)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with(self.email_from, self.pswd)
        mock_server.sendmail.assert_called_once()
        mock_server.sendmail.assert_called_with(self.email_from, self.email_to, ANY)
        self.assertIn(self.email_to, mock_server.sendmail.call_args[0][1])

    @patch('smtplib.SMTP')
    def test_send_clinc_email_exception(self, mock_smtp):
        # Mock the SMTP server to raise an exception
        mock_smtp.side_effect = smtplib.SMTPException("Failed to connect")

        with self.assertRaises(smtplib.SMTPException) as e:
            send_email_to_clinic(self.server, self.port, self.email_from, self.email_to, 
                                self.pswd, self.attachment_name, self.attachment_content,
                                self.patient_name, self.patient_email, self.datetime)        
            self.assertEqual(str(e.exception), "Failed to connect")
        
    @patch('smtplib.SMTP')
    def test_send_clinic_email_message_content(self, mock_smtp):
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        pdf_content = base64.b64encode(b'test that content is correct\nTest1\nTest2').decode('utf-8')
        # Call the send_emails function
        send_email_to_clinic(self.server, self.port, self.email_from, self.email_to, 
                        self.pswd, self.attachment_name, pdf_content,
                        self.patient_name, self.patient_email, self.datetime)

        # Get the email content
        email_content = mock_server.sendmail.call_args[0][2]
        
        # Check if the email content is correctly formed
        self.assertIn("Content-Type: text/html", email_content)
        self.assertIn("Subject: Patient Consent Form Submission", email_content)
        self.assertIn("<strong>Patient Name:</strong> Bob Marley", email_content)

class TestSendPatientEmails(unittest.TestCase):
    def setUp(self) -> None:
        self.server = "smtp.gmail.com"
        self.port = 587
        self.email_from = "anullpointers@gmail.com"
        self.email_to = "z5361148@ad.unsw.edu.au"
        self.pswd = "jrowigmvzvtoifhz"
        self.patient_name = 'Bob Marley'

        
    @patch('smtplib.SMTP')
    def test_send_patient_email_success(self, mock_smtp):
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Call the send_emails function
        send_email_to_patient(self.server, self.port, self.email_from, self.email_to, 
                             self.pswd, self.patient_name)

        # Assertions to check if email sending process is called correctly
        mock_smtp.assert_called_with(self.server, self.port)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with(self.email_from, self.pswd)
        mock_server.sendmail.assert_called_once()
        mock_server.sendmail.assert_called_with(self.email_from, self.email_to, ANY)
        self.assertIn(self.email_to, mock_server.sendmail.call_args[0][1])

    @patch('smtplib.SMTP')
    def test_send_patient_email_exception(self, mock_smtp):
        # Mock the SMTP server to raise an exception
        mock_smtp.side_effect = smtplib.SMTPException("Failed to connect")

        with self.assertRaises(smtplib.SMTPException) as e:
            send_email_to_patient(self.server, self.port, self.email_from, self.email_to, 
                             self.pswd, self.patient_name)      
            self.assertEqual(str(e.exception), "Failed to connect")
        
    @patch('smtplib.SMTP')
    def test_send_patient_email_message_content(self, mock_smtp):
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        # Call the send_emails function
        send_email_to_patient(self.server, self.port, self.email_from, self.email_to, 
                             self.pswd, self.patient_name)

        # Get the email content
        email_content = mock_server.sendmail.call_args[0][2]
        
        # Check if the email content is correctly formed
        self.assertIn("Content-Type: text/html", email_content)
        self.assertIn("Subject: Confirmation of Consent Form Submission - UNSW Optometry Clinic", email_content)
        self.assertIn("Dear Bob Marley,", email_content)    
    


if __name__ == '__main__':
    unittest.main()