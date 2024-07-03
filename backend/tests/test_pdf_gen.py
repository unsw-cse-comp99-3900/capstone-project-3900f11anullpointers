
import unittest
import os
from unittest.mock import MagicMock, patch
from fpdf import FPDF
import logging
import json

from src.fonts.fonts import Fonts
import src.pdf_gen
from src.pdf_gen import (
    GeneratePDF
)
class testPDFGeneration(unittest.TestCase):
    def setUp(self) -> None:
        self.pdf = MagicMock(spec=FPDF)
        self.generator = GeneratePDF()

    @patch('pdf_gen.FPDF')
    @patch('fonts.fonts.Fonts')
    @patch('pdf_gen.open', read_data='{"document": "Sample document text"}')
    @patch('pdf_gen.datetime')
    def test_generate_pdf(self, mock_fpdf, mock_fonts, mock_open, mock_datetime):
        # Setup mocks
        mock_datetime.now.return_value.strftime.return_value = '01 January 2023'
        pdf_instance = mock_fpdf.return_value

        # Mocking the Fonts instantiation
        fonts_instance = MagicMock()
        mock_fonts.return_value = fonts_instance

        # Creating instance of GeneratePDF
        pdf_generator = GeneratePDF()

        # Test data
        token = 'test1'
        client_name = 'ur mom'
        form_name = 'adult'
        consent_flags = [True, False, True]

        # Call the method under test
        pdf_generator.generate_pdf(token, client_name, form_name, consent_flags)

        # Assertions to verify interactions
        pdf_instance.image.assert_called()
        pdf_instance.image.assert_any_call('logo/logo.png', w=25, x=15, y=11)
        pdf_instance.cell.assert_any_call(0, 5, txt='', ln=True)
        pdf_instance.image.assert_any_call(f'signatures/{token}.png', h=20)
        pdf_instance.cell.assert_any_call(0, 5, txt=client_name, ln=True, align='L')
        pdf_instance.cell.assert_any_call(0, 5, txt='01 January 2023', ln=True, align='L')
        pdf_instance.output.assert_called_once_with(f'{token}.pdf')

        mock_open.assert_called_once_with(f'texts/{form_name}.json', 'r', encoding='utf-8')
        mock_datetime.now.return_value.strftime.assert_called_once_with('%d %B %Y')
        logging.info.assert_called_once_with('%s.pdf successfully generated', token)

    def test_invalid_flags(self):
        with self.assertRaises(Exception):
            self.generator.generate_pdf("test", "Gerald", "adult", ['a', 1, 4])   

    def test_empty_flags(self):
        with self.assertRaises(Exception):
            self.generator.generate_pdf("test", "Gerald", "adult", [])
    
    def test_incorrect_amount_of_flags(self):
        with self.assertRaises(Exception):
            self.generator.generate_pdf("test", "Gerald", "adult", [False, False])
        
        with self.assertRaises(Exception):
            self.generator.generate_pdf("test", "Gerald", "adult", [False, False, True, True])
    
    def test_invalid_form_type(self):
        with self.assertRaises(FileNotFoundError):
            self.generator.generate_pdf("test", "Gerald", "lol", [True, True, True])
        
 
        

class testGeneratePDFInit(unittest.TestCase):

    def setUp(self) -> None:
        self.fonts_mock = MagicMock(spec=Fonts)
        self.generator_mock = MagicMock(spec=GeneratePDF)
        self.generator_mock.pdf = MagicMock(spec=FPDF) 
        self.generator_mock.Fonts = MagicMock(spec=Fonts)

    @patch('src.fonts.fonts.Fonts')
    @patch('src.pdf_gen.FPDF')
    def test_init_successful(self, mock_fonts, mock_fpdf):
        """Test successful initialization of GeneratePDF"""
        mock_fonts.return_value = MagicMock()
        instance = GeneratePDF()
        self.assertIsInstance(instance, GeneratePDF)
        mock_fpdf.assert_called_once()
        mock_fonts.assert_called_once()


    @patch('src.pdf_gen.Fonts')
    @patch('logging.error')
    def test_init_runtime_error(self, MockFonts, mock_logging_error):
        MockFonts.return_value = self.fonts_mock
        self.generator_mock.Fonts.side_effect = FileNotFoundError("fonts/font_config.json not found")
        
        with self.assertRaises(FileNotFoundError):
            GeneratePDF()       
        mock_logging_error.assert_called_with("Cannot read fonts/font_config.json config file: fonts/font_config.json not found")

    @patch('src.pdf_gen.Fonts')
    @patch('logging.error')
    def test_init_file_not_found_error(self, MockFonts, mock_logging_error):
        MockFonts.return_value = self.fonts_mock
        self.fonts_mock.side_effect = FileNotFoundError("Fonts configuration file not found")
        
        with self.assertRaises(FileNotFoundError):
            self.generator_mock = GeneratePDF()

        mock_logging_error.assert_called_with("PDF generator cannot be made: Fonts configuration file not found")

    @patch('src.pdf_gen.Fonts')
    @patch('logging.error')
    def test_init_json_decode_error(self, MockFonts, mock_logging_error):
        MockFonts.return_value = self.fonts_mock
        self.fonts_mock.side_effect = json.JSONDecodeError("JSON decode error", "", 0)
        
        with self.assertRaises(json.JSONDecodeError):
            self.generator_mock = GeneratePDF()

        mock_logging_error.assert_called_with("PDF generator cannot be made: JSON decode error")

     
if __name__ == '__main__':
    unittest.main()