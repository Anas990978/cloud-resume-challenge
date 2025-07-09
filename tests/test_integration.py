import unittest
import requests
import json
import time

class TestAPIIntegration(unittest.TestCase):
    """Integration tests for the API Gateway and Lambda function"""
    
    def setUp(self):
        self.api_url = "https://5xwzjw1xh6.execute-api.us-east-1.amazonaws.com/prod/visitors"
        self.timeout = 10  # seconds
    
    def test_api_endpoint_accessibility(self):
        """Test that the API endpoint is accessible"""
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            self.assertEqual(response.status_code, 200)
        except requests.exceptions.RequestException as e:
            self.fail(f"API endpoint not accessible: {e}")
    
    def test_api_response_format(self):
        """Test that the API returns the expected JSON format"""
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            self.assertEqual(response.status_code, 200)
            
            # Test content type
            self.assertEqual(response.headers.get('content-type'), 'application/json')
            
            # Test JSON structure
            data = response.json()
            self.assertIn('count', data)
            self.assertIsInstance(data['count'], int)
            self.assertGreaterEqual(data['count'], 1)
            
        except requests.exceptions.RequestException as e:
            self.fail(f"API request failed: {e}")
        except json.JSONDecodeError as e:
            self.fail(f"Invalid JSON response: {e}")
    
    def test_cors_headers(self):
        """Test that CORS headers are properly configured"""
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            self.assertEqual(response.status_code, 200)
            
            # Check CORS headers
            self.assertIn('access-control-allow-origin', 
                         [h.lower() for h in response.headers.keys()])
            
            cors_header = response.headers.get('Access-Control-Allow-Origin')
            self.assertEqual(cors_header, '*')
            
        except requests.exceptions.RequestException as e:
            self.fail(f"CORS test failed: {e}")
    
    def test_visitor_counter_increment(self):
        """Test that the visitor counter increments on multiple requests"""
        try:
            # Make first request
            response1 = requests.get(self.api_url, timeout=self.timeout)
            self.assertEqual(response1.status_code, 200)
            count1 = response1.json()['count']
            
            # Wait a moment
            time.sleep(1)
            
            # Make second request
            response2 = requests.get(self.api_url, timeout=self.timeout)
            self.assertEqual(response2.status_code, 200)
            count2 = response2.json()['count']
            
            # Counter should have incremented
            self.assertEqual(count2, count1 + 1)
            
        except requests.exceptions.RequestException as e:
            self.fail(f"Counter increment test failed: {e}")
    
    def test_api_performance(self):
        """Test that the API responds within acceptable time limits"""
        start_time = time.time()
        
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            end_time = time.time()
            
            response_time = end_time - start_time
            
            self.assertEqual(response.status_code, 200)
            self.assertLess(response_time, 5.0)  # Should respond within 5 seconds
            
        except requests.exceptions.RequestException as e:
            self.fail(f"Performance test failed: {e}")

class TestWebsiteIntegration(unittest.TestCase):
    """Integration tests for the website"""
    
    def setUp(self):
        self.website_urls = [
            "https://d1hmohpegyvejg.cloudfront.net",
            "https://anas-webiste.com"
        ]
    
    def test_website_accessibility(self):
        """Test that the website is accessible"""
        for url in self.website_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    # At least one URL should work
                    self.assertIn("<!DOCTYPE html", response.text)
                    self.assertIn("Anas Tarek", response.text)
                    return
            except requests.exceptions.RequestException:
                continue
        
        self.fail("None of the website URLs are accessible")
    
    def test_visitor_counter_on_website(self):
        """Test that the visitor counter is present on the website"""
        for url in self.website_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    self.assertIn("visitor-count", response.text)
                    self.assertIn("Site Visitors", response.text)
                    return
            except requests.exceptions.RequestException:
                continue
        
        self.fail("Visitor counter not found on website")

if __name__ == '__main__':
    unittest.main()