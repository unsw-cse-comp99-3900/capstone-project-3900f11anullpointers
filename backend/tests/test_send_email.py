"""Module for testing classes in send_email.py"""
import unittest
import smtplib
import base64
import os
from datetime import datetime
from unittest.mock import patch, MagicMock, ANY
from src.send_email import SendEmail
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))
load_dotenv(find_dotenv(".env.local"))

SERVER: str = os.getenv("SMTP_HOST")
PORT: str = os.getenv("SMTP_PORT")
SMTP_USER: str = os.getenv("SMTP_USER")
PSWD: str = os.getenv("SMTP_PSWD")

class TestSendClinicEmails(unittest.TestCase):
    """
    Unit tests for the `send_email_to_clinic` function.
    """

    def setUp(self) -> None:
        """
        Sets up the test environment with common parameters used across tests.
        """
        self.send_email = SendEmail(SERVER, PORT, SMTP_USER, PSWD)
        self.email_to = "no@email.com"
        self.attachment_name = "bobs_consent_info.pdf"
        self.attachment_content = base64.b64encode(b"pdf content test bobby").decode("utf-8")
        self.patient_name = "Bob Marley"
        self.patient_email = "no@email.com"
        self.datetime = datetime.now()

    @patch("src.send_email.smtplib.SMTP")
    def test_send_clinic_email_success(self, mock_smtp):
        """
        Tests that the `send_email_to_clinic` function sends an email successfully.
        """
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Call the send_email_to_clinic method
        self.send_email.send_email_to_clinic(self.email_to, self.attachment_name,
                                            self.attachment_content, self.patient_name,
                                            self.patient_email, self.datetime)

        # Assertions to verify that the email sending process was called correctly
        mock_smtp.assert_called_with(SERVER, PORT)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with(SMTP_USER, PSWD)
        mock_server.sendmail.assert_called_once()
        mock_server.sendmail.assert_called_with(SMTP_USER, self.email_to, ANY)
        self.assertIn(self.email_to, mock_server.sendmail.call_args[0][1])

    @patch("src.send_email.smtplib.SMTP")
    def test_send_clinic_email_authentication_error(self, mock_smtp):
        """Tests if SMTPAuthenticationError is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPAuthenticationError(1, "error")

        with self.assertRaises(smtplib.SMTPAuthenticationError):
            self.send_email.send_email_to_clinic(self.email_to, self.attachment_name,
                                                 self.attachment_content, self.patient_name,
                                                 self.patient_email, self.datetime)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_clinic_email_connect_error(self, mock_smtp):
        """Tests if SMTPConnectError is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPConnectError(1, "error")

        with self.assertRaises(smtplib.SMTPConnectError):
            self.send_email.send_email_to_clinic(self.email_to, self.attachment_name,
                                                 self.attachment_content, self.patient_name,
                                                 self.patient_email, self.datetime)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_clinic_email_helo_error(self, mock_smtp):
        """Tests if SMTPHeloError is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPHeloError(1, "error")

        with self.assertRaises(smtplib.SMTPHeloError):
            self.send_email.send_email_to_clinic(self.email_to, self.attachment_name,
                                                 self.attachment_content, self.patient_name,
                                                 self.patient_email, self.datetime)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_clinic_email_sender_refused(self, mock_smtp):
        """Tests if SMTPSenderRefused is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPSenderRefused(1, b"error", "bob")

        with self.assertRaises(smtplib.SMTPSenderRefused):
            self.send_email.send_email_to_clinic(self.email_to, self.attachment_name,
                                                 self.attachment_content, self.patient_name,
                                                 self.patient_email, self.datetime)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_clinic_email_recipients_refused(self, mock_smtp):
        """Tests if SMTPRecipientsRefused is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPRecipientsRefused("bob")

        with self.assertRaises(smtplib.SMTPRecipientsRefused):
            self.send_email.send_email_to_clinic(self.email_to, self.attachment_name,
                                                 self.attachment_content, self.patient_name,
                                                 self.patient_email, self.datetime)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_clinic_email_data_error(self, mock_smtp):
        """Tests if SMTPDataError is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPDataError(1, "error")

        with self.assertRaises(smtplib.SMTPDataError):
            self.send_email.send_email_to_clinic(self.email_to, self.attachment_name,
                                                 self.attachment_content, self.patient_name,
                                                 self.patient_email, self.datetime)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_clinic_email_not_supported_error(self, mock_smtp):
        """Tests if SMTPNotSupportedError is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPNotSupportedError(1, "error")

        with self.assertRaises(smtplib.SMTPNotSupportedError):
            self.send_email.send_email_to_clinic(self.email_to, self.attachment_name,
                                                 self.attachment_content, self.patient_name,
                                                 self.patient_email, self.datetime)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_clinic_email_server_disconnected(self, mock_smtp):
        """Tests if SMTPServerDisconnected is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPServerDisconnected(1, "error")

        with self.assertRaises(smtplib.SMTPServerDisconnected):
            self.send_email.send_email_to_clinic(self.email_to, self.attachment_name,
                                                 self.attachment_content, self.patient_name,
                                                 self.patient_email, self.datetime)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_clinic_email_smtp_exception(self, mock_smtp):
        """Tests if SMTPException is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPException(1, "error")

        with self.assertRaises(smtplib.SMTPException):
            self.send_email.send_email_to_clinic(self.email_to, self.attachment_name,
                                                 self.attachment_content, self.patient_name,
                                                 self.patient_email, self.datetime)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_clinic_email_message_content(self, mock_smtp):
        """
        Tests that the `send_email_to_clinic` function sends an email with the correct content.
        """
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Call the send_email_to_clinic function
        self.send_email.send_email_to_clinic(self.email_to, self.attachment_name,
                                             self.attachment_content, self.patient_name,
                                             self.patient_email, self.datetime)

        # Get the email content
        email_content = mock_server.sendmail.call_args[0][2]

        # Check if the email content is correctly formed
        self.assertIn("Content-Type: text/html", email_content)
        self.assertIn("Subject: Patient Consent Form Submission", email_content)
        self.assertIn("Bob Marley", email_content)

class TestSendPatientEmails(unittest.TestCase):
    """
    Unit tests for the `send_email_to_patient` function.
    """

    def setUp(self) -> None:
        """
        Sets up the test environment with common parameters used across tests.
        """
        self.send_email = SendEmail(SERVER, PORT, SMTP_USER, PSWD)
        self.email_from = SMTP_USER
        self.email_to = "no@email.com"
        self.patient_name = "Bob Marley"

    @patch("src.send_email.smtplib.SMTP")
    def test_send_patient_email_success(self, mock_smtp):
        """
        Tests that the `send_email_to_patient` function sends an email successfully.
        """
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Call the send_email_to_patient function
        self.send_email.send_email_to_patient(self.email_to, self.patient_name)

        # Assertions to verify that the email sending process was called correctly
        mock_smtp.assert_called_with(SERVER, PORT)
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_with(self.email_from, PSWD)
        mock_server.sendmail.assert_called_once()
        mock_server.sendmail.assert_called_with(self.email_from, self.email_to, ANY)
        self.assertIn(self.email_to, mock_server.sendmail.call_args[0][1])

    @patch("src.send_email.smtplib.SMTP")
    def test_send_patient_email_authentication_error(self, mock_smtp):
        """Tests if SMTPAuthenticationError is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPAuthenticationError(1, "error")

        with self.assertRaises(smtplib.SMTPAuthenticationError):
            self.send_email.send_email_to_patient(self.email_to, self.patient_name)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_patient_email_connect_error(self, mock_smtp):
        """Tests if SMTPConnectError is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPConnectError(1, "error")

        with self.assertRaises(smtplib.SMTPConnectError):
            self.send_email.send_email_to_patient(self.email_to, self.patient_name)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_patient_email_helo_error(self, mock_smtp):
        """Tests if SMTPHeloError is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPHeloError(1, "error")

        with self.assertRaises(smtplib.SMTPHeloError):
            self.send_email.send_email_to_patient(self.email_to, self.patient_name)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_patient_email_sender_refused(self, mock_smtp):
        """Tests if SMTPSenderRefused is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPSenderRefused(1, b"error", "bob")

        with self.assertRaises(smtplib.SMTPSenderRefused):
            self.send_email.send_email_to_patient(self.email_to, self.patient_name)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_patient_email_recipients_refused(self, mock_smtp):
        """Tests if SMTPRecipientsRefused is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPRecipientsRefused("bob")

        with self.assertRaises(smtplib.SMTPRecipientsRefused):
            self.send_email.send_email_to_patient(self.email_to, self.patient_name)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_patient_email_data_error(self, mock_smtp):
        """Tests if SMTPDataError is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPDataError(1, "error")

        with self.assertRaises(smtplib.SMTPDataError):
            self.send_email.send_email_to_patient(self.email_to, self.patient_name)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_patient_email_not_supported_error(self, mock_smtp):
        """Tests if SMTPNotSupportedError is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPNotSupportedError(1, "error")

        with self.assertRaises(smtplib.SMTPNotSupportedError):
            self.send_email.send_email_to_patient(self.email_to, self.patient_name)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_patient_email_server_disconnected(self, mock_smtp):
        """Tests if SMTPServerDisconnected is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPServerDisconnected(1, "error")

        with self.assertRaises(smtplib.SMTPServerDisconnected):
            self.send_email.send_email_to_patient(self.email_to, self.patient_name)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_patient_email_smtp_exception(self, mock_smtp):
        """Tests if SMTPException is handled correctly"""
        mock_smtp.side_effect = smtplib.SMTPException(1, "error")

        with self.assertRaises(smtplib.SMTPException):
            self.send_email.send_email_to_patient(self.email_to, self.patient_name)

    @patch("src.send_email.smtplib.SMTP")
    def test_send_patient_email_message_content(self, mock_smtp):
        """
        Tests that the `send_email_to_patient` function sends an email with the correct content.
        """
        # Mock the SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        # Call the send_email_to_patient function
        self.send_email.send_email_to_patient(self.email_to, self.patient_name)

        # Get the email content
        email_content = mock_server.sendmail.call_args[0][2]

        # Check if the email content is correctly formed
        self.assertIn("Content-Type: text/html", email_content)
        self.assertIn(
            "Subject: Confirmation of Consent Form Submission - UNSW Optometry Clinic",
            email_content,
        )
        self.assertIn("Dear Bob Marley,", email_content)

if __name__ == "__main__":
    unittest.main()
