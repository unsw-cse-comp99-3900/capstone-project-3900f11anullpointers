import unittest
from unittest.mock import patch, MagicMock, ANY
import smtplib, base64
from datetime import datetime
from src.send_email import send_email_to_clinic, send_email_to_patient

class TestSendClinicEmails(unittest.TestCase):
    """
    Unit tests for the `send_email_to_clinic` function.
    """

    def setUp(self) -> None:
        """
        Sets up the test environment with common parameters used across tests.
        """
        self.server = "smtp.gmail.com"
        self.port = 587
        self.email_from = "anullpointers@gmail.com"
        self.email_to = "z5361148@ad.unsw.edu.au"
        self.pswd = "jrowigmvzvtoifhz"
        self.attachment_name = "bobs_consent_info.pdf"
        self.attachment_content = base64.b64encode(b'pdf content test bobby').decode('utf-8')
        self.patient_name = 'Bob Marley'
        self.patient_email = "z5361148@ad.unsw.edu.au"
        self.datetime = datetime.now()

    @patch('src.send_email.smtplib.SMTP')
    def test_send_clinic_email_success(self, mock_smtp):
        """
        Tests that the `send_email_to_clinic` function sends an email successfully.
        """
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Call the send_email_to_clinic function
        send_email_to_clinic(
            self.server, self.port, self.email_from, self.email_to, 
            self.pswd, self.attachment_name, self.attachment_content,
            self.patient_name, self.patient_email, self.datetime
        )

        # Assertions to verify that the email sending process was called correctly
        mock_smtp.assert_called_with(self.server, self.port)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with(self.email_from, self.pswd)
        mock_server.sendmail.assert_called_once()
        mock_server.sendmail.assert_called_with(self.email_from, self.email_to, ANY)
        self.assertIn(self.email_to, mock_server.sendmail.call_args[0][1])

    @patch('src.send_email.smtplib.SMTP')
    def test_send_clinic_email_exception(self, mock_smtp):
        """
        Tests that the `send_email_to_clinic` function handles SMTP exceptions correctly.
        """
        # Mock the SMTP server to raise an exception
        mock_smtp.side_effect = smtplib.SMTPHeloError(1, "Failed to connect")

        with self.assertRaises(smtplib.SMTPHeloError) as e:
            send_email_to_clinic(
                self.server, self.port, self.email_from, self.email_to, 
                self.pswd, self.attachment_name, self.attachment_content,
                self.patient_name, self.patient_email, self.datetime
            )
        
        self.assertEqual(str(e.exception.args[1]), "Failed to connect")

    @patch('src.send_email.smtplib.SMTP')
    def test_send_clinic_email_message_content(self, mock_smtp):
        """
        Tests that the `send_email_to_clinic` function sends an email with the correct content.
        """
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Call the send_email_to_clinic function
        send_email_to_clinic(
            self.server, self.port, self.email_from, self.email_to, 
            self.pswd, self.attachment_name, self.attachment_content,
            self.patient_name, self.patient_email, self.datetime
        )

        # Get the email content
        email_content = mock_server.sendmail.call_args[0][2]
        
        # Check if the email content is correctly formed
        self.assertIn("Content-Type: text/html", email_content)
        self.assertIn("Subject: Patient Consent Form Submission", email_content)
        self.assertIn("<strong>Patient Name:</strong> Bob Marley", email_content)

class TestSendPatientEmails(unittest.TestCase):
    """
    Unit tests for the `send_email_to_patient` function.
    """

    def setUp(self) -> None:
        """
        Sets up the test environment with common parameters used across tests.
        """
        self.server = "smtp.gmail.com"
        self.port = 587
        self.email_from = "anullpointers@gmail.com"
        self.email_to = "z5361148@ad.unsw.edu.au"
        self.pswd = "jrowigmvzvtoifhz"
        self.patient_name = 'Bob Marley'

    @patch('src.send_email.smtplib.SMTP')
    def test_send_patient_email_success(self, mock_smtp):
        """
        Tests that the `send_email_to_patient` function sends an email successfully.
        """
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Call the send_email_to_patient function
        send_email_to_patient(self.server, self.port, self.email_from, self.email_to, 
                              self.pswd, self.patient_name)

        # Assertions to verify that the email sending process was called correctly
        mock_smtp.assert_called_with(self.server, self.port)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with(self.email_from, self.pswd)
        mock_server.sendmail.assert_called_once()
        mock_server.sendmail.assert_called_with(self.email_from, self.email_to, ANY)
        self.assertIn(self.email_to, mock_server.sendmail.call_args[0][1])

    @patch('src.send_email.smtplib.SMTP')
    def test_send_patient_email_exception(self, mock_smtp):
        """
        Tests that the `send_email_to_patient` function handles SMTP exceptions correctly.
        """
        # Mock the SMTP server to raise an exception
        mock_smtp.side_effect = smtplib.SMTPHeloError(1, "Failed to connect")

        with self.assertRaises(smtplib.SMTPHeloError) as e:
            send_email_to_patient(self.server, self.port, self.email_from, self.email_to, 
                                  self.pswd, self.patient_name)
        
        self.assertEqual(str(e.exception.args[1]), "Failed to connect")

    @patch('src.send_email.smtplib.SMTP')
    def test_send_patient_email_message_content(self, mock_smtp):
        """
        Tests that the `send_email_to_patient` function sends an email with the correct content.
        """
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Call the send_email_to_patient function
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
