import unittest
from app import app, calculate_risk_score, calculate_graph_y_position, calculate_graph_height


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_get(self):
        # Test GET request to the index route
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Country Threat Weights', response.data)

    def test_index_post_valid_data(self):
        # Test POST request to the index route with valid data
        data = {
            'Canada_ddos_weight': '3',
            'Canada_phishing_weight': '4',
            'Canada_physical_attack_weight': '2',
            'Canada_cloud_security_weight': '3',
            'India_ddos_weight': '4',
            'India_phishing_weight': '5',
            'India_physical_attack_weight': '3',
            'India_cloud_security_weight': '2',
        }
        response = self.app.post('/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Results', response.data)

    def test_index_post_invalid_country(self):
        # Test POST request to the index route with an invalid country
        data = {
            'InvalidCountry_ddos_weight': '3',
            'InvalidCountry_phishing_weight': '4',
            'InvalidCountry_physical_attack_weight': '2',
            'InvalidCountry_cloud_security_weight': '3',
        }
        response = self.app.post('/', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Invalid country selected.', response.data)

    def test_calculate_risk_score(self):
        # Test the calculate_risk_score function
        threat_model = {"DDoS": 3, "Phishing": 4, "PhysicalAttack": 2, "CloudSecurity": 3}
        country = "Canada"
        risk_score = calculate_risk_score(threat_model, country)
        self.assertEqual(risk_score, 3.17)

    def test_calculate_graph_y_position(self):
        # Test the calculate_graph_y_position function
        y_position = calculate_graph_y_position(4)
        self.assertEqual(y_position, 168.6)

    def test_calculate_graph_height(self):
        # Test the calculate_graph_height function
        height = calculate_graph_height(3)
        self.assertEqual(height, 84.3)


if __name__ == '__main__':
    unittest.main()
