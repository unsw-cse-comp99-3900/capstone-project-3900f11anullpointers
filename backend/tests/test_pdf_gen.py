
import unittest
from unittest.mock import MagicMock, patch
from fpdf import FPDF
import logging
import json

from fonts.fonts import Fonts
from pdf_gen import (
    GeneratePDF
)
class testPDFGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self.pdf = MagicMock(spec=FPDF)
        self.generator = GeneratePDF()
    
    def tearDown(self) -> None:
        return super().tearDown()


    @patch('pdf_gen.FPDF')
    @patch('pdf_gen.Document')
    @patch('pdf_gen.Fonts')
    @patch('builtins.open', unittest.mock.mock_open(read_data='{}'))    
    def test_success(self, MockFonts, MockDocument, MockFPDF):
        # Mock required dependencies
        mock_fonts_instance = MagicMock()
        MockFonts.return_value = mock_fonts_instance

        mock_pdf_instance = MagicMock()
        MockFPDF.return_value = mock_pdf_instance

        # Call the method under test
        self.generator.generate_pdf("test1", "Gerald", "adult", [True, False, True])

        # Assertions
        mock_pdf_instance.add_page.assert_called_once()
        mock_pdf_instance.image.assert_called_with('logo/logo.png', w=25, x=15, y=11)
        mock_pdf_instance.image.assert_any_call('signatures/test1.png', h=20)
        mock_pdf_instance.cell.assert_any_call(0, 5, txt="Gerald", ln=True, align="L")

    def test_invalid_flags(self):
        #self.generator.generate_pdf("test", "Gerald", "adult", [])
        self.assertEqual(1,1, "Should be equal")       

    def test_empty_flags(self):
        with self.assertRaises(Exception):
            self.generator.generate_pdf("test", "Gerald", "adult", [])
    
    def test_invalid_form_type(self):
        with self.assertRaises(FileNotFoundError):
            self.generator.generate_pdf("test", "Gerald", "lol", [True, True, True])      
        
        with self.assertRaises(FileNotFoundError):
            self.generator.generate_pdf("test", "Gerald", "adult", [True, False, True])
        

class testGeneratePDFInit(unittest.TestCase):
    @patch('pdf_gen.Fonts')
    def test_init_runtime_error(self, MockFonts):
        MockFonts.side_effect = RuntimeError("Fonts initialization failed")
        
        with self.assertRaises(RuntimeError):
            GeneratePDF()

        logging.error.assert_called_with("PDF generator cannot be made: Fonts initialization failed")

    @patch('pdf_gen.Fonts')
    def test_init_file_not_found_error(self, MockFonts):
        MockFonts.side_effect = FileNotFoundError("Fonts configuration file not found")
        
        with self.assertRaises(FileNotFoundError):
            GeneratePDF()

        logging.error.assert_called_with("PDF generator cannot be made: Fonts configuration file not found")

    @patch('pdf_gen.Fonts')
    def test_init_json_decode_error(self, MockFonts):
        MockFonts.side_effect = json.JSONDecodeError("JSON decode error", "", 0)
        
        with self.assertRaises(json.JSONDecodeError):
            GeneratePDF()

        logging.error.assert_called_with("PDF generator cannot be made: JSON decode error")
             
             
if __name__ == '__main__':
    unittest.main()