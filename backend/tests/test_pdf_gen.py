"""Module to test the pdf_gen.py file"""
import unittest
import json
import logging
import base64
from unittest.mock import MagicMock, patch, mock_open
from datetime import datetime
from fpdf import FPDF
from src.fonts.fonts import Fonts
from src.pdf_gen import (
    GeneratePDF
)

VALID_SIGNATURE = (
    "data:image/png;base64,"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1Pe"
    "AAAADElEQVQI12P4//8/AAX+Av7czFnnAAAAAElFTkSuQmCC"
)

logging.disable(logging.CRITICAL)

class TestWorkingGeneration(unittest.TestCase):
    """
    Test suite for the `GeneratePDF` class to ensure that 
    PDF generation works for both "adult" and "child" types.
    """

    def test_working_adult(self):
        """
        Tests that the `generate_pdf` method works correctly for an "adult" form type.
        Ensures no unexpected exceptions are raised.
        """
        try:
            generator = GeneratePDF()
            generator.generate_pdf("test1", "adult", [True, True, False],
                                   VALID_SIGNATURE, datetime.now())
        except Exception:
            self.fail("Unexpected failure")

    def test_working_child(self):
        """
        Tests that the `generate_pdf` method works correctly for a "child" form type.
        Ensures no unexpected exceptions are raised.
        """
        try:
            generator = GeneratePDF()
            generator.generate_pdf("test2", "child", [True, False], VALID_SIGNATURE, datetime.now())
        except Exception:
            self.fail("Unexpected failure")

class TestGeneratePDFInit(unittest.TestCase):
    """
    Test suite for the initialization of the `GeneratePDF` class.
    """

    def setUp(self):
        """
        Sets up the test environment by patching the `Fonts` class used in `GeneratePDF`.
        """
        self.patcher = patch("src.pdf_gen.Fonts")
        self.mock_fonts = self.patcher.start()

    def tearDown(self):
        """
        Cleans up the test environment by stopping the patch started in `setUp`.
        """
        self.patcher.stop()

    def test_init_successful(self):
        """
        Tests successful initialization of `GeneratePDF` when `Fonts` is mocked successfully.
        """
        self.mock_fonts.return_value = MagicMock(spec=Fonts)
        instance = GeneratePDF()
        self.assertIsInstance(instance, GeneratePDF)
        self.mock_fonts.assert_called_once()

    def test_init_runtime_error(self):
        """
        Tests that `GeneratePDF` raises a `RuntimeError` when `Fonts` raises a `RuntimeError`.
        """
        self.mock_fonts.side_effect = RuntimeError("fonts/font_config.json not found")
        with self.assertRaises(RuntimeError):
            GeneratePDF()

    def test_init_file_not_found_error(self):
        """
        Tests that `GeneratePDF` raises a `FileNotFoundError`
        when `Fonts` raises a `FileNotFoundError`.
        """
        self.mock_fonts.side_effect = FileNotFoundError("Fonts configuration file not found")
        with self.assertRaises(FileNotFoundError):
            GeneratePDF()

    def test_init_json_decode_error(self):
        """
        Tests that `GeneratePDF` raises a `JSONDecodeError` when `Fonts` raises a `JSONDecodeError`.
        """
        self.mock_fonts.side_effect = json.JSONDecodeError("JSON decode error", "", 0)
        with self.assertRaises(json.JSONDecodeError):
            GeneratePDF()

class TestPDFGeneration(unittest.TestCase):
    """
    Test suite for the `generate_pdf` method of the `GeneratePDF` class.
    """
    def setUp(self) -> None:
        """
        Sets up the test environment by creating a mock 
        `FPDF` object and an instance of `GeneratePDF`.
        """
        self.pdf = MagicMock(spec=FPDF)
        self.generator = GeneratePDF()
        self.timestamp = datetime.fromisocalendar(2000,1,1)

    def test_generate_pdf_output(self):
        """
        Verifies that the `generate_pdf` method produces a PDF containing a specific substring.
        """
        pdf = self.generator.generate_pdf("test", "adult", [True, False, True],
                                          VALID_SIGNATURE, self.timestamp)

        decoded_pdf = base64.b64decode(pdf)
        self.assertTrue(decoded_pdf.startswith(b"%PDF-"))

    def test_successful_pdf_generation(self):
        """
        Tests that the `generate_pdf` method completes successfully
        and that the `pdf` attribute is an instance of `FPDF`.
        """
        self.generator.generate_pdf("bob marley", "adult", [True, True, False],
                                    VALID_SIGNATURE, self.timestamp)
        self.assertIsInstance(self.generator.pdf, FPDF)

    def test_invalid_form_type(self):
        """
        Tests that `generate_pdf` raises a `FileNotFoundError` when an invalid form type is provided
        """
        with self.assertRaises(FileNotFoundError):
            self.generator.generate_pdf("bob marley", "lol", [True, True, False],
                                        VALID_SIGNATURE, self.timestamp)

    def test_invalid_signature(self):
        """
        Tests that `generate_pdf` raises an exception when an invalid signature is provided.
        """
        with self.assertRaises(Exception):
            self.generator.generate_pdf("bob marley", "adult", [False, True, True],
                                        "invalid signature", self.timestamp)

class TestGetJSON(unittest.TestCase):
    """
    Test suite for the `_get_json_dict` method of the `GeneratePDF` class.
    """

    def setUp(self):
        """
        Sets up the test environment by creating an instance of 
        `GeneratePDF` and setting parameters for testing.
        """
        self.generator = GeneratePDF()
        self.token = "test_token"
        self.client_name = "John Doe"
        self.form_name = "test_form"
        self.consent_flags = [True, False, True]

    @patch("builtins.open", new_callable=mock_open, read_data='{"document": "Sample text"}')
    def test_get_json_dict(self, mock_file):
        """
        Tests that `_get_json_dict` correctly reads and parses a JSON file.
        """
        result = self.generator._get_json_dict(self.form_name)
        self.assertEqual(result, {"document": "Sample text"})

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_get_json_dict_file_not_found(self, mock_file):
        """
        Tests that `_get_json_dict` raises a `FileNotFoundError` when the file does not exist.
        """
        with self.assertRaises(FileNotFoundError):
            self.generator._get_json_dict(self.form_name)

    @patch("builtins.open", new_callable=mock_open, read_data="invalid json")
    def test_get_json_dict_json_decode_error(self, mock_file):
        """
        Tests that `_get_json_dict` raises a `JSONDecodeError` when the file contains invalid JSON.
        """
        with self.assertRaises(json.JSONDecodeError):
            self.generator._get_json_dict(self.form_name)

if __name__ == "__main__":
    unittest.main()
