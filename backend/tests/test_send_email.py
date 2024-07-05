import unittest
from unittest.mock import patch, MagicMock, ANY
from io import BytesIO
import smtplib
from src.send_email import send_emails 

class TestSendEmails(unittest.TestCase):
    
    @patch('smtplib.SMTP')
    def test_send_emails_success(self, mock_smtp):
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        server = "smtp.gmail.com"
        port = 587
        email_from = "anullpointers@gmail.com"
        email_to = "z5361148@ad.unsw.edu.au"
        pswd = "rtrjqzvtyuecbyxh"
        attachment_name = "src/test1.pdf"
        attachment_content = BytesIO(b"PDF content")
        
        # Call the send_emails function
        send_emails(server, port, email_from, email_to, pswd, attachment_name, attachment_content)

        # Assertions to check if email sending process is called correctly
        mock_smtp.assert_called_with(server, port)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with(email_from, pswd)
        mock_server.sendmail.assert_called_once()
        mock_server.sendmail.assert_called_with(email_from, email_to, ANY)
        self.assertIn(email_to, mock_server.sendmail.call_args[0][1])

    @patch('smtplib.SMTP')
    def test_send_emails_exception(self, mock_smtp):
        # Mock the SMTP server to raise an exception
        mock_smtp.side_effect = smtplib.SMTPException("Failed to connect")
        
        server = "smtp.example.com"
        port = 587
        email_from = "sender@example.com"
        email_to = "recipient@example.com"
        pswd = "password"
        attachment_name = "consent_form.pdf"
        attachment_content = BytesIO(b"PDF content")

        with self.assertRaises(smtplib.SMTPException) as e:
            send_emails(server, port, email_from, email_to, pswd, attachment_name, attachment_content)
        self.assertEqual(str(e.exception), "Failed to connect")
        
    @patch('smtplib.SMTP')
    def test_send_emails_message_content(self, mock_smtp):
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        server = "smtp.example.com"
        port = 587
        email_from = "sender@example.com"
        email_to = "recipient@example.com"
        pswd = "password"
        attachment_name = "consent_form.pdf"
        attachment_content = BytesIO(b"PDF content")
        
        # Call the send_emails function
        send_emails(server, port, email_from, email_to, pswd, attachment_name, attachment_content)

        # Get the email content
        email_content = mock_server.sendmail.call_args[0][2]
        
        # Check if the email content is correctly formed
        self.assertIn("Content-Type: text/html", email_content)
        self.assertIn("Subject: Patient consent form", email_content)
        self.assertIn("Dear [Recipient's Name],", email_content)


if __name__ == '__main__':
    unittest.main()