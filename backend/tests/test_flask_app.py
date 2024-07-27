import unittest
from unittest.mock import patch
import app
import logging

valid_signature = (
'data:image/png;base64,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'
)
invalid_signature = "invalid signature"

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
            "drawSignature": valid_signature,
            "formType": "adult",
            "consent": {
                "researchConsent": True,
                "contactConsent": True,
                "studentConsent": False
            }
        }

        # Ensure that actual emails are not sent while testing 
        self.patcher = patch('app._send_emails')
        self.mock_send_emails = self.patcher.start()
        self.mock_send_emails.return_value = None
        
    def test_post_method_success(self):
        """
        Tests that a valid payload results in a successful form submission.
        """
        response = self.client.post('/post', json=self.payload)
        self.assertIn(b"Form submission successful", response.data)
        self.assertEqual(response.status_code, 200)
    
    def test_post_method_empty_consent_flags(self):
        """
        Tests that an empty consent flags field results in an internal server error.
        """
        self.payload['consent'] = {}
        response = self.client.post('/post', json=self.payload)
        self.assertEqual(response.status_code, 500)

    def test_post_method_missing_consent_flags(self):
        """
        Tests that missing consent flags results in an internal server error.
        """
        self.payload['consent'] = {
            "contactConsent": True,
            "studentConsent": False
        }
        response = self.client.post('/post', json=self.payload)
        self.assertEqual(response.status_code, 500)

    def test_post_method_invalid_signature(self):
        """
        Tests that an invalid signature results in an internal server error.
        """
        self.payload['drawSignature'] = invalid_signature
        response = self.client.post('/post', json=self.payload)
        self.assertEqual(response.status_code, 500)
    
    def test_post_method_invalid_form_type(self):
        """
        Tests that an invalid form type results in an internal server error.
        """
        self.payload['formType'] = "lol"
        response = self.client.post('/post', json=self.payload)
        self.assertEqual(response.status_code, 500)
    
    def test_post_method_empty_payload(self):
        """
        Tests that an empty payload results in an internal server error.
        """
        self.payload = {}
        response = self.client.post('/post', json=self.payload)
        self.assertEqual(response.status_code, 500)
    
if __name__ == "__main__":
    unittest.main()