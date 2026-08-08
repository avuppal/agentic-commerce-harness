import unittest
import requests
from unittest.mock import patch, Mock
from src.sige.authenticity_checker import verify

class TestAuthenticityChecker(unittest.TestCase):

    @patch('src.sige.authenticity_checker.requests.get')
    def test_verify_successful_match(self, mock_get):
        """
        Test case for when the Verified by GS1 API returns a matching brand owner.
        """
        # 1. Setup the mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        # Mocking the json() method to return a specific dictionary
        mock_response.json.return_value = {
            "companyName": "Example Brand Co.",
            "gcp": "0123456789",
            "status": "active"
        }
        mock_get.return_value = mock_response

        # 2. Define the input product data
        product_data = {
            "gtin": "01234567890123",
            "gs1:brandOwner": [
                {
                    "@type": "gs1:Organization",
                    "gs1:brandName": "Example Brand Co."
                }
            ]
        }

        # 3. Call the function and assert the outcome
        result = verify(product_data)
        
        self.assertEqual(result['verification_status'], 'verified')
        self.assertTrue(result['gtin_verified'])
        self.assertIn('latency_ms', result) # Check if latency is recorded
        # Assert that the mock was called with the correct GTIN
        mock_get.assert_called_once_with('https://api.gs1.org/verify/gtin/01234567890123', headers={'Authorization': 'Bearer None'}, timeout=10)

    @patch('src.sige.authenticity_checker.requests.get')
    def test_verify_failed_mismatch(self, mock_get):
        """
        Test case for when the API returns a different brand owner, indicating a counterfeit risk.
        """
        # 1. Setup the mock API response for a mismatch
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "companyName": "Different Company Inc.",
            "gcp": "9876543210",
            "status": "active"
        }
        mock_get.return_value = mock_response

        # 2. Define the input product data
        product_data = {
            "gtin": "01234567890123",
            "gs1:brandOwner": [
                {
                    "@type": "gs1:Organization",
                    "gs1:brandName": "Example Brand Co."
                }
            ]
        }

        # 3. Call the function and assert the counterfeit risk outcome
        result = verify(product_data)
        
        self.assertEqual(result['verification_status'], 'failed')
        self.assertIn('Brand owner mismatch', result['details'])
        self.assertTrue(result['gtin_verified'])
        mock_get.assert_called_once()

    @patch('src.sige.authenticity_checker.requests.get')
    def test_verify_missing_gtin(self, mock_get):
        """
        Test case for when the product data is missing the GTIN.
        """
        product_data = {
            "gs1:brandOwner": [
                {
                    "@type": "gs1:Organization",
                    "gs1:brandName": "Example Brand Co."
                }
            ]
        }

        result = verify(product_data)
        
        self.assertEqual(result['verification_status'], 'error')
        self.assertIn('Missing GTIN or brandOwner', result['reason'])
        mock_get.assert_not_called()

    @patch('src.sige.authenticity_checker.requests.get')
    def test_verify_missing_brand_owner(self, mock_get):
        """
        Test case for when the product data is missing the brand owner.
        """
        product_data = {
            "gtin": "01234567890123"
        }

        result = verify(product_data)
        
        self.assertEqual(result['verification_status'], 'error')
        self.assertIn('Missing GTIN or brandOwner', result['reason'])
        mock_get.assert_not_called()

    @patch('src.sige.authenticity_checker.requests.get')
    def test_verify_api_error(self, mock_get):
        """
        Test case for when the Verified by GS1 API returns an error.
        """
        # 1. Setup the mock API response to simulate an error
        mock_response = Mock()
        mock_response.status_code = 500 # Simulate server error
        mock_get.return_value = mock_response

        # 2. Define the input product data
        product_data = {
            "gtin": "01234567890123",
            "gs1:brandOwner": [
                {
                    "@type": "gs1:Organization",
                    "gs1:brandName": "Example Brand Co."
                }
            ]
        }

        # 3. Call the function and assert the error outcome
        result = verify(product_data)
        
        self.assertEqual(result['verification_status'], 'error')
        self.assertIn('GS1 API Error:', result['reason'])
        mock_get.assert_called_once()

    @patch('src.sige.authenticity_checker.requests.get')
    def test_verify_api_timeout(self, mock_get):
        """
        Test case for when the Verified by GS1 API call times out.
        """
        # Configure the mock_get to raise a Timeout exception
        mock_get.side_effect = requests.exceptions.Timeout

        # 2. Define the input product data
        product_data = {
            "gtin": "01234567890123",
            "gs1:brandOwner": [
                {
                    "@type": "gs1:Organization",
                    "gs1:brandName": "Example Brand Co."
                }
            ]
        }

        # 3. Call the function and assert the error outcome
        result = verify(product_data)
        
        self.assertEqual(result['verification_status'], 'error')
        self.assertIn('API request timed out', result['reason'])
        mock_get.assert_called_once()

    @patch('src.sige.authenticity_checker.query_verified_by_gs1')
    def test_verify_mock_response_match(self, mock_query_verified_by_gs1):
        """
        Test case for when the mock GS1 API response indicates a match.
        """
        # Setup mock to return a known mock response for a specific GTIN
        mock_query_verified_by_gs1.return_value = {
            "companyName": "The Coca-Cola Company",
            "gcp": "096619",
            "status": "active"
        }

        product_data = {
            "gtin": "096619756805", # Example GTIN for Coca-Cola
            "gs1:brandOwner": [
                {
                    "@type": "gs1:Organization",
                    "gs1:brandName": "The Coca-Cola Company"
                }
            ]
        }

        result = verify(product_data)
        
        self.assertEqual(result['verification_status'], 'verified')
        mock_query_verified_by_gs1.assert_called_once_with("096619756805")

    @patch('src.sige.authenticity_checker.query_verified_by_gs1')
    def test_verify_mock_response_mismatch(self, mock_query_verified_by_gs1):
        """
        Test case for when the mock GS1 API response indicates a mismatch.
        """
        # Setup mock to return a known mock response for a specific GTIN
        mock_query_verified_by_gs1.return_value = {
            "companyName": "Faux Cola Company",
            "gcp": "123456",
            "status": "active"
        }

        product_data = {
            "gtin": "096619756805", # Example GTIN for Coca-Cola
            "gs1:brandOwner": [
                {
                    "@type": "gs1:Organization",
                    "gs1:brandName": "The Coca-Cola Company"
                }
            ]
        }

        result = verify(product_data)
        
        self.assertEqual(result['verification_status'], 'failed')
        self.assertIn('Brand owner mismatch', result['details'])
        mock_query_verified_by_gs1.assert_called_once_with("096619756805")

    @patch('src.sige.authenticity_checker.query_verified_by_gs1')
    def test_verify_mock_response_not_found(self, mock_query_verified_by_gs1):
        """
        Test case for when the mock GS1 API does not find the GTIN.
        """
        mock_query_verified_by_gs1.return_value = {
            "error": "GTIN not found in mock database"
        }

        product_data = {
            "gtin": "00000000000000", # Non-existent GTIN
            "gs1:brandOwner": [
                {
                    "@type": "gs1:Organization",
                    "gs1:brandName": "Some Brand"
                }
            ]
        }

        result = verify(product_data)
        
        self.assertEqual(result['verification_status'], 'error')
        self.assertIn('GS1 API Error:', result['reason'])
        mock_query_verified_by_gs1.assert_called_once_with("00000000000000")

# This allows the test to be run from the command line
if __name__ == '__main__':
    unittest.main()
