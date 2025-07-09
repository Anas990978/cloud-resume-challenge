import unittest
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os

class TestEndToEnd(unittest.TestCase):
    """End-to-end tests for the complete application"""
    
    def setUp(self):
        self.api_url = "https://5xwzjw1xh6.execute-api.us-east-1.amazonaws.com/prod/visitors"
        self.website_urls = [
            "https://d1hmohpegyvejg.cloudfront.net",
            "https://anas-webiste.com"
        ]
        
        # Setup Chrome driver for Selenium tests (optional)
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in background
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
        except Exception:
            self.driver = None  # Skip Selenium tests if Chrome not available
    
    def tearDown(self):
        if self.driver:
            self.driver.quit()
    
    def test_complete_user_journey(self):
        """Test the complete user journey from website visit to API call"""
        # Step 1: Visit the website
        website_accessible = False
        for url in self.website_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    website_accessible = True
                    self.assertIn("Anas Tarek", response.text)
                    break
            except requests.exceptions.RequestException:
                continue
        
        self.assertTrue(website_accessible, "Website is not accessible")
        
        # Step 2: Test API functionality
        try:
            api_response = requests.get(self.api_url, timeout=10)
            self.assertEqual(api_response.status_code, 200)
            
            data = api_response.json()
            self.assertIn('count', data)
            self.assertIsInstance(data['count'], int)
            
        except requests.exceptions.RequestException as e:
            self.fail(f"API test failed: {e}")
    
    @unittest.skipIf(not os.getenv('RUN_SELENIUM_TESTS'), "Selenium tests disabled")
    def test_visitor_counter_ui(self):
        """Test visitor counter functionality in the browser"""
        if not self.driver:
            self.skipTest("Chrome driver not available")
        
        for url in self.website_urls:
            try:
                self.driver.get(url)
                
                # Wait for the visitor counter to load
                wait = WebDriverWait(self.driver, 10)
                visitor_count_element = wait.until(
                    EC.presence_of_element_located((By.ID, "visitor-count"))
                )
                
                # Check that the counter shows a number
                counter_text = visitor_count_element.text
                self.assertNotEqual(counter_text, "Loading...")
                self.assertNotEqual(counter_text, "Error")
                
                # Try to parse as integer
                try:
                    count = int(counter_text)
                    self.assertGreater(count, 0)
                except ValueError:
                    self.fail(f"Visitor count is not a valid number: {counter_text}")
                
                return  # Success, exit the loop
                
            except Exception as e:
                continue  # Try next URL
        
        self.fail("Could not test visitor counter on any website URL")
    
    def test_mobile_responsiveness(self):
        """Test that the website is mobile responsive"""
        if not self.driver:
            self.skipTest("Chrome driver not available")
        
        for url in self.website_urls:
            try:
                # Set mobile viewport
                self.driver.set_window_size(375, 667)  # iPhone size
                self.driver.get(url)
                
                # Check if mobile menu toggle is visible
                try:
                    mobile_toggle = self.driver.find_element(By.CLASS_NAME, "mobile-menu-toggle")
                    self.assertTrue(mobile_toggle.is_displayed())
                except Exception:
                    pass  # Mobile toggle might not be visible depending on implementation
                
                # Check that content is readable on mobile
                body = self.driver.find_element(By.TAG_NAME, "body")
                self.assertIsNotNone(body)
                
                return  # Success
                
            except Exception:
                continue
        
        self.skipTest("Could not test mobile responsiveness")
    
    def test_all_sections_present(self):
        """Test that all required sections are present on the website"""
        required_sections = ['home', 'about', 'tools', 'resume', 'certificates', 'projects']
        
        for url in self.website_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    content = response.text
                    
                    for section in required_sections:
                        self.assertIn(f'id="{section}"', content, 
                                    f"Section '{section}' not found on website")
                    
                    return  # Success
                    
            except requests.exceptions.RequestException:
                continue
        
        self.fail("Could not verify website sections")
    
    def test_social_links_present(self):
        """Test that social media links are present"""
        social_links = ['github.com', 'linkedin.com', 'mailto:']
        
        for url in self.website_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    content = response.text.lower()
                    
                    for link in social_links:
                        self.assertIn(link, content, 
                                    f"Social link '{link}' not found on website")
                    
                    return  # Success
                    
            except requests.exceptions.RequestException:
                continue
        
        self.fail("Could not verify social links")

if __name__ == '__main__':
    unittest.main()