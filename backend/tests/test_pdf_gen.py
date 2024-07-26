
import unittest
import os
from unittest.mock import MagicMock, patch, mock_open
from fpdf import FPDF
import logging
import json
from datetime import datetime

from src.fonts.fonts import Fonts
import src.pdf_gen
from src.pdf_gen import (
    GeneratePDF
)

class PlsWork(unittest.TestCase):
    def test_working(self):
        generator = GeneratePDF()
        generator.generate_pdf('test1', 'name', 'adult', [True, True, False], datetime.now())

# class testGeneratePDFInit(unittest.TestCase):

#     def setUp(self) -> None:
#         self.fonts_mock = MagicMock(spec=Fonts)
#         self.generator_mock = MagicMock(spec=GeneratePDF)
#         self.generator_mock.pdf = MagicMock(spec=FPDF) 
#         self.generator_mock.Fonts = MagicMock(spec=Fonts)

#     @patch('src.fonts.fonts.Fonts')
#     @patch('src.pdf_gen.FPDF')
#     def test_init_successful(self, mock_fonts, mock_fpdf):
#         """Test successful initialization of GeneratePDF"""
#         mock_fonts.return_value = MagicMock()
#         instance = GeneratePDF()
#         self.assertIsInstance(instance, GeneratePDF)
#         mock_fpdf.assert_called_once()
#         mock_fonts.assert_called_once()


#     @patch('src.pdf_gen.Fonts')
#     @patch('logging.error')
#     def test_init_runtime_error(self, MockFonts, mock_logging_error):
#         MockFonts.return_value = self.fonts_mock
#         self.generator_mock.Fonts.side_effect = FileNotFoundError("fonts/font_config.json not found")
        
#         with self.assertRaises(FileNotFoundError):
#             GeneratePDF()       
#         mock_logging_error.assert_called_with("Cannot read fonts/font_config.json config file: fonts/font_config.json not found")

#     @patch('src.pdf_gen.Fonts')
#     @patch('logging.error')
#     def test_init_file_not_found_error(self, MockFonts, mock_logging_error):
#         MockFonts.return_value = self.fonts_mock
#         self.fonts_mock.side_effect = FileNotFoundError("Fonts configuration file not found")
        
#         with self.assertRaises(FileNotFoundError):
#             self.generator_mock = GeneratePDF()

#         mock_logging_error.assert_called_with("PDF generator cannot be made: Fonts configuration file not found")

#     @patch('src.pdf_gen.Fonts')
#     @patch('logging.error')
#     def test_init_json_decode_error(self, MockFonts, mock_logging_error):
#         MockFonts.return_value = self.fonts_mock
#         self.fonts_mock.side_effect = json.JSONDecodeError("JSON decode error", "", 0)
        
#         with self.assertRaises(json.JSONDecodeError):
#             self.generator_mock = GeneratePDF()

#         mock_logging_error.assert_called_with("PDF generator cannot be made: JSON decode error")

# class testPDFGeneration(unittest.TestCase):
#     def setUp(self) -> None:
#         self.pdf = MagicMock(spec=FPDF)
#         self.generator = GeneratePDF()

#     @patch('pdf_gen.FPDF')
#     @patch('fonts.fonts.Fonts')
#     @patch('pdf_gen.open', read_data='{"document": "Sample document text"}')
#     @patch('pdf_gen.datetime')
#     def test_generate_pdf(self, mock_fpdf, mock_fonts, mock_open, mock_datetime):
#         # Setup mocks
#         mock_datetime.now.return_value.strftime.return_value = '01 January 2023'
#         pdf_instance = mock_fpdf.return_value

#         # Mocking the Fonts instantiation
#         fonts_instance = MagicMock()
#         mock_fonts.return_value = fonts_instance

#         # Creating instance of GeneratePDF
#         pdf_generator = GeneratePDF()

#         # Test data
#         token = 'test1'
#         client_name = 'Gerald'
#         form_name = 'adult'
#         consent_flags = [True, False, True]

#         # Call the method under test
#         pdf_generator.generate_pdf(token, client_name, form_name, consent_flags)

#         # Assertions to verify interactions
#         pdf_instance.image.assert_called()
#         pdf_instance.output.assert_called_once_with(f'{token}.pdf')

#         mock_open.assert_called_once_with(f'texts/{form_name}.json', 'r', encoding='utf-8')
#         logging.info.assert_called_once_with('%s.pdf successfully generated', token)

    
#     def test_successful_pdf_generation(self):
#         generator = GeneratePDF()
#         generator.generate_pdf('token', 'name', 'adult', [True, True, False])
#         self.assertIsInstance(generator.pdf, FPDF)
        
#     def test_invalid_flags(self):
#         with self.assertRaises(Exception):
#             self.generator.generate_pdf("test", "Gerald", "adult", ['a', 1, 4])   

#     def test_empty_flags(self):
#         with self.assertRaises(Exception):
#             self.generator.generate_pdf("test", "Gerald", "adult", [])
    
#     def test_incorrect_amount_of_flags(self):
#         with self.assertRaises(Exception):
#             self.generator.generate_pdf("test", "Gerald", "adult", [False, False])
        
#         with self.assertRaises(Exception):
#             self.generator.generate_pdf("test", "Gerald", "adult", [False, False, True, True])
    
#     def test_invalid_form_type(self):
#         with self.assertRaises(FileNotFoundError):
#             self.generator.generate_pdf("test", "Gerald", "lol", [True, True, True])
        
# class testGetJSON(unittest.TestCase):

#     def setUp(self):
#         self.pdf_generator = GeneratePDF()
#         self.token = "test_token"
#         self.client_name = "John Doe"
#         self.form_name = "test_form"
#         self.consent_flags = [True, False, True]

#     @patch("builtins.open", new_callable=mock_open, read_data='{"document": "Sample document text"}')
#     def test_get_json_dict(self, mock_file):
#         result = self.pdf_generator._get_json_dict(self.form_name)
#         self.assertEqual(result, {"document": "Sample document text"})

#     @patch("builtins.open", side_effect=FileNotFoundError)
#     def test_get_json_dict_file_not_found(self, mock_file):
#         with self.assertRaises(FileNotFoundError):
#             self.pdf_generator._get_json_dict(self.form_name)

#     @patch("builtins.open", new_callable=mock_open, read_data='invalid json')
#     def test_get_json_dict_json_decode_error(self, mock_file):
#         with self.assertRaises(json.JSONDecodeError):
#             self.pdf_generator._get_json_dict(self.form_name)

# if __name__ == '__main__':
#     unittest.main()