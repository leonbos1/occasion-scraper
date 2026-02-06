import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utills.responses import ErrorCodes


class TestAPIErrorHandling(unittest.TestCase):
    """Test error handling for validation, not found, and database errors"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock Flask's jsonify to return a simple dict wrapper
        self.jsonify_patcher = patch('utills.responses.jsonify')
        self.mock_jsonify = self.jsonify_patcher.start()
        
        def jsonify_side_effect(data):
            """Mock jsonify that returns an object with get_json method"""
            mock_response = MagicMock()
            mock_response.get_json.return_value = data
            return mock_response
        
        self.mock_jsonify.side_effect = jsonify_side_effect

    def tearDown(self):
        """Clean up after tests"""
        self.jsonify_patcher.stop()

    def test_validation_error_response_structure(self):
        """Test that validation errors return correct structure"""
        from utills.responses import validation_error
        
        response, status_code = validation_error("Name is required")
        response_data = response.get_json()
        
        self.assertEqual(status_code, 400)
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"]["code"], ErrorCodes.VALIDATION_ERROR)
        self.assertIn("Name is required", response_data["error"]["message"])

    def test_not_found_error_response_structure(self):
        """Test that not found errors return correct structure"""
        from utills.responses import not_found_error
        
        response, status_code = not_found_error("Car not found")
        response_data = response.get_json()
        
        self.assertEqual(status_code, 404)
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"]["code"], ErrorCodes.NOT_FOUND)
        self.assertIn("Car not found", response_data["error"]["message"])

    def test_database_error_response_structure(self):
        """Test that database errors return correct structure"""
        from utills.responses import database_error
        
        response, status_code = database_error("Connection timeout")
        response_data = response.get_json()
        
        self.assertEqual(status_code, 500)
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"]["code"], ErrorCodes.DATABASE_ERROR)
        self.assertIn("Connection timeout", response_data["error"]["message"])

    def test_generic_error_response_structure(self):
        """Test that generic errors return correct structure"""
        from utills.responses import error_response
        
        response, status_code = error_response(
            ErrorCodes.INTERNAL_ERROR, 
            "Something went wrong", 
            500
        )
        response_data = response.get_json()
        
        self.assertEqual(status_code, 500)
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"]["code"], ErrorCodes.INTERNAL_ERROR)
        self.assertEqual(response_data["error"]["message"], "Something went wrong")

    def test_success_response_structure(self):
        """Test that success responses return correct structure"""
        from utills.responses import success_response
        
        test_data = {"cars": [{"id": "1", "brand": "Toyota"}]}
        response, status_code = success_response(test_data)
        response_data = response.get_json()
        
        self.assertEqual(status_code, 200)
        self.assertTrue(response_data["success"])
        self.assertEqual(response_data["data"], test_data)

    def test_success_response_with_metadata(self):
        """Test that success responses can include metadata"""
        from utills.responses import success_response
        
        test_data = {"cars": []}
        metadata = {"total": 100, "page": 1}
        response, status_code = success_response(test_data, metadata)
        response_data = response.get_json()
        
        self.assertEqual(status_code, 200)
        self.assertTrue(response_data["success"])
        self.assertEqual(response_data["data"], test_data)
        self.assertEqual(response_data["metadata"], metadata)

    def test_error_response_with_details(self):
        """Test that error responses can include additional details"""
        from utills.responses import error_response
        
        response, status_code = error_response(
            ErrorCodes.VALIDATION_ERROR,
            "Multiple fields invalid",
            400,
            {"fields": ["name", "email"]}
        )
        response_data = response.get_json()
        
        self.assertEqual(status_code, 400)
        self.assertFalse(response_data["success"])
        self.assertEqual(response_data["error"]["details"]["fields"], ["name", "email"])

    def test_all_error_codes_defined(self):
        """Test that all standard error codes are defined"""
        self.assertEqual(ErrorCodes.VALIDATION_ERROR, "VALIDATION_ERROR")
        self.assertEqual(ErrorCodes.NOT_FOUND, "NOT_FOUND")
        self.assertEqual(ErrorCodes.AUTH_ERROR, "AUTH_ERROR")
        self.assertEqual(ErrorCodes.DATABASE_ERROR, "DATABASE_ERROR")
        self.assertEqual(ErrorCodes.INTERNAL_ERROR, "INTERNAL_ERROR")

    def test_validation_error_with_field_details(self):
        """Test validation error can include field-specific information"""
        from utills.responses import validation_error
        
        response, status_code = validation_error(
            "Invalid input",
            {"required_fields": ["brand", "model"]}
        )
        response_data = response.get_json()
        
        self.assertEqual(status_code, 400)
        self.assertEqual(response_data["error"]["code"], ErrorCodes.VALIDATION_ERROR)
        self.assertIn("required_fields", response_data["error"]["details"])

    def test_error_messages_are_user_friendly(self):
        """Test that error messages don't expose technical details"""
        from utills.responses import database_error
        
        response, status_code = database_error("Database operation failed")
        response_data = response.get_json()
        
        # Message should not contain stack traces or SQL
        message = response_data["error"]["message"]
        self.assertNotIn("Traceback", message)
        self.assertNotIn("SELECT", message)
        self.assertNotIn("Exception", message)


if __name__ == '__main__':
    unittest.main()
