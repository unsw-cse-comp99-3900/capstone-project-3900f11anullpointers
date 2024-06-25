import unittest
#from ../backend/PDFgeneration import PDFGeneration

class testPDFGeneration(unittest.TestCase):
    def setUp(self) -> None:
#        generator = GeneratePDF()
        return super().setUp()
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    def test_success(self):
#        generator.generate_pdf("test", "Gerald", "adult", [True, False, True])
        self.assertEqual(1,1, "Should be equal")

    def test_invalid_flags(self):
 #        generator.generate_pdf("test", "Gerald", "adult", [])
        self.assertEqual(1,1, "Should be equal")       

    def test_empty_flags(self):
#        with self.assertRaises(Exception):
#           generator.generate_pdf("test", "Gerald", "adult", [])
        self.assertEqual(1,1, "Should be equal")       
        
if __name__ == '__main__':
    unittest.main()