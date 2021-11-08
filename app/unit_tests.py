import unittest

target = __import__("app")

class TestPopulation(unittest.TestCase):
    def test_census_data(self):
        """
        Test that method returns expected population
        given lat / long inputs
        """
        lat = "47.6062"
        long = "-122.3321"
        county, population, density = target.get_census_data(lat, long)
        self.assertEqual(population, 2252782)
    
    def test_ip_to_zip(self):
        """
        Test that ip to zipcode translation works
        """
        test_ip = "8.8.8.8"
        zipcode, country, lat, lng = target.get_location_by_ip(test_ip)
        self.assertEqual(zipcode, "20149")

if __name__ == '__main__':
    unittest.main()