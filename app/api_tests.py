import unittest

target = __import__("app")

class TestPopulation(unittest.TestCase):
    def test_get_country_code_by_ip(self):
        """
        Test that method returns expected country
        """
        ip_address = "8.8.8.8"
        expected = "US"
        cc = target.get_country_code_by_ip(ip_address)
        self.assertEqual(cc, expected)    

if __name__ == '__main__':
    unittest.main()