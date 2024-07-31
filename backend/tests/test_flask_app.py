"""Module to test the app.py file which acts as a flask server"""
import unittest
from unittest.mock import patch
import logging
import app

VALID_SIGNATURE = (
    "data:image/png;base64,"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1Pe"
    "AAAADElEQVQI12P4//8/AAX+Av7czFnnAAAAAElFTkSuQmCC"
)
INVALID_SIGNATURE = "invalid signature"

class FlaskAppTests(unittest.TestCase):
    """
    Unit tests for the Flask application to ensure proper handling of form submissions.
    """
    @classmethod
    def setUpClass(cls):
        """
        Sets up the test client and disables logging for a cleaner test output.
        """
        cls.client = app.app.test_client()
        cls.client.testing = True
        logging.disable(logging.CRITICAL)

    def setUp(self) -> None:
        """
        Initializes a valid payload for testing and mocks the send_emails function
        to prevent actual emails from being sent during tests.
        """
        self.payload = {
            "name": "Bob Marley",
            "email": "bobmarley@example.com",
            "drawSignature": VALID_SIGNATURE,
            "formType": "adult",
            "consent": {
                "researchConsent": True,
                "contactConsent": True,
                "studentConsent": False
            }
        }

        # Ensure that actual emails are not sent while testing
        self.patcher = patch("app._send_emails")
        self.mock_send_emails = self.patcher.start()
        self.mock_send_emails.return_value = None

    def test_post_method_success(self):
        """
        Tests that a valid payload results in a successful form submission.
        """
        response = self.client.post("/post", json=self.payload)
        self.assertIn(b"Form submission successful", response.data)
        self.assertEqual(response.status_code, 200)

    def test_post_method_empty_consent_flags(self):
        """
        Tests that an empty consent flags field results in an internal server error.
        """
        self.payload["consent"] = {}
        response = self.client.post("/post", json=self.payload)
        self.assertEqual(response.status_code, 500)

    def test_post_method_missing_consent_flags(self):
        """
        Tests that missing consent flags results in an internal server error.
        """
        self.payload["consent"] = {
            "contactConsent": True,
            "studentConsent": False
        }
        response = self.client.post("/post", json=self.payload)
        self.assertEqual(response.status_code, 500)

    def test_post_method_invalid_signature(self):
        """
        Tests that an invalid signature results in an internal server error.
        """
        self.payload["drawSignature"] = INVALID_SIGNATURE
        response = self.client.post("/post", json=self.payload)
        self.assertEqual(response.status_code, 500)

    def test_post_method_invalid_form_type(self):
        """
        Tests that an invalid form type results in an internal server error.
        """
        self.payload["formType"] = "lol"
        response = self.client.post("/post", json=self.payload)
        self.assertEqual(response.status_code, 500)

    def test_post_method_empty_payload(self):
        """
        Tests that an empty payload results in an internal server error.
        """
        self.payload = {}
        response = self.client.post("/post", json=self.payload)
        self.assertEqual(response.status_code, 500)

if __name__ == "__main__":
    unittest.main()