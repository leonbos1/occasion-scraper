import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We need to mock the database session and logger before importing
sys.modules['backend.extensions'] = MagicMock()
sys.modules['backend.utills.logger'] = MagicMock()
sys.modules['backend.models.car'] = MagicMock()
sys.modules['backend.models.scrape_session'] = MagicMock()
sys.modules['backend.models.blueprint'] = MagicMock()


class TestScraperEdgeCases(unittest.TestCase):
    """Test scraper edge cases like no cars found and page fetch failures"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock the logger
        self.mock_logger = MagicMock()
        self.mock_logger.log_info = MagicMock()
        self.mock_logger.log_error = MagicMock()
        self.mock_logger.log_warning = MagicMock()

    @patch('scrapers.autoscout_fast.requests.get')
    @patch('scrapers.autoscout_fast._logger')
    def test_no_cars_found_scenario(self, mock_logger, mock_requests_get):
        """Test scraper returns empty list when no cars are found"""
        from scrapers.autoscout_fast import scrape_page
        
        # Set up mock logger
        mock_logger.log_info = MagicMock()
        mock_logger.log_error = MagicMock()
        
        # Mock response with HTML that has no article elements
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <div class="no-results">No cars found matching your criteria</div>
            </body>
        </html>
        """
        mock_requests_get.return_value = mock_response
        
        # Mock scrape session
        mock_scrape_session = MagicMock()
        mock_scrape_session.id = "test-session-123"
        
        # Call scrape_page
        result = scrape_page("http://test.com", mock_scrape_session)
        
        # Verify empty list is returned
        self.assertEqual(result, [])
        self.assertIsInstance(result, list)
        
        # Verify appropriate logging occurred
        mock_logger.log_info.assert_called()
        # Check that a log about no articles was made
        log_calls = [str(call) for call in mock_logger.log_info.call_args_list]
        self.assertTrue(any("No article elements found" in str(call) or "0 cars" in str(call) 
                           for call in log_calls))

    @patch('scrapers.autoscout_fast.requests.get')
    @patch('scrapers.autoscout_fast._logger')
    def test_page_fetch_failure_non_200_status(self, mock_logger, mock_requests_get):
        """Test scraper returns empty list and logs error on HTTP non-200 status"""
        from scrapers.autoscout_fast import scrape_page
        
        # Set up mock logger
        mock_logger.log_error = MagicMock()
        
        # Mock response with 404 status
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response
        
        # Mock scrape session
        mock_scrape_session = MagicMock()
        mock_scrape_session.id = "test-session-456"
        
        # Call scrape_page
        result = scrape_page("http://test.com/nonexistent", mock_scrape_session)
        
        # Verify empty list is returned
        self.assertEqual(result, [])
        
        # Verify error was logged
        mock_logger.log_error.assert_called()
        error_calls = [str(call) for call in mock_logger.log_error.call_args_list]
        self.assertTrue(any("404" in str(call) or "HTTP" in str(call) 
                           for call in error_calls))

    @patch('scrapers.autoscout_fast.requests.get')
    @patch('scrapers.autoscout_fast._logger')
    def test_page_fetch_network_failure(self, mock_logger, mock_requests_get):
        """Test scraper returns empty list and logs error on network failure"""
        from scrapers.autoscout_fast import scrape_page
        import requests
        
        # Set up mock logger
        mock_logger.log_error = MagicMock()
        
        # Mock network exception
        mock_requests_get.side_effect = requests.exceptions.ConnectionError("Network unreachable")
        
        # Mock scrape session
        mock_scrape_session = MagicMock()
        mock_scrape_session.id = "test-session-789"
        
        # Call scrape_page
        result = scrape_page("http://test.com", mock_scrape_session)
        
        # Verify empty list is returned
        self.assertEqual(result, [])
        
        # Verify error was logged
        mock_logger.log_error.assert_called()
        error_calls = [str(call) for call in mock_logger.log_error.call_args_list]
        self.assertTrue(any("Network" in str(call) or "error" in str(call).lower() 
                           for call in error_calls))

    @patch('scrapers.autoscout_fast.requests.get')
    @patch('scrapers.autoscout_fast._logger')
    def test_page_fetch_timeout(self, mock_logger, mock_requests_get):
        """Test scraper returns empty list and logs error on timeout"""
        from scrapers.autoscout_fast import scrape_page
        import requests
        
        # Set up mock logger
        mock_logger.log_error = MagicMock()
        
        # Mock timeout exception
        mock_requests_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        # Mock scrape session
        mock_scrape_session = MagicMock()
        mock_scrape_session.id = "test-session-timeout"
        
        # Call scrape_page
        result = scrape_page("http://test.com", mock_scrape_session)
        
        # Verify empty list is returned
        self.assertEqual(result, [])
        
        # Verify error was logged
        mock_logger.log_error.assert_called()

    @patch('scrapers.autoscout_fast.requests.get')
    @patch('scrapers.autoscout_fast._logger')
    def test_html_parsing_failure(self, mock_logger, mock_requests_get):
        """Test scraper handles malformed HTML gracefully"""
        from scrapers.autoscout_fast import scrape_page
        
        # Set up mock logger
        mock_logger.log_error = MagicMock()
        mock_logger.log_info = MagicMock()
        
        # Mock response with malformed HTML
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body><article incomplete"
        mock_requests_get.return_value = mock_response
        
        # Mock scrape session
        mock_scrape_session = MagicMock()
        mock_scrape_session.id = "test-session-parse"
        
        # Call scrape_page - should not crash
        result = scrape_page("http://test.com", mock_scrape_session)
        
        # Verify it returns a list (empty or with parsed items)
        self.assertIsInstance(result, list)


if __name__ == '__main__':
    unittest.main()
