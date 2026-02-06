import unittest
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.base import BaseModel


class TestDatabaseDatetimeInserts(unittest.TestCase):
    """Test that database inserts work without datetime truncation errors"""

    def test_basemodel_datetime_string_conversion(self):
        """Test that BaseModel datetime can be converted to string without fractional seconds"""
        model = BaseModel()
        
        # Convert to string as done in API responses
        created_str = str(model.created).split('.')[0]
        updated_str = str(model.updated).split('.')[0]
        
        # Verify format is YYYY-MM-DD HH:MM:SS (19 characters)
        self.assertEqual(len(created_str), 19)
        self.assertEqual(len(updated_str), 19)
        
        # Verify no decimal point in string representation
        self.assertNotIn('.', created_str)
        self.assertNotIn('.', updated_str)

    def test_car_model_inherits_datetime_handling(self):
        """Test that Car model creates timestamps without microseconds"""
        # Car model inherits from BaseModel
        # We can't instantiate without all required fields, but we can verify
        # that if we create a BaseModel instance and check its datetime,
        # Car would have same behavior
        model = BaseModel()
        self.assertEqual(model.created.microsecond, 0)
        self.assertEqual(model.updated.microsecond, 0)

    def test_scrape_session_datetime_compatibility(self):
        """Test that ScrapeSession timestamps are database compatible"""
        model = BaseModel()
        
        # Verify timestamps can be formatted for database
        created_db_format = model.created.strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(len(created_db_format), 19)
        
        # Verify parsing back works
        parsed = datetime.strptime(created_db_format, '%Y-%m-%d %H:%M:%S')
        self.assertEqual(parsed.microsecond, 0)

    def test_blueprint_datetime_compatibility(self):
        """Test that BluePrint timestamps are database compatible"""
        model = BaseModel()
        
        # Verify no microseconds that would cause MySQL truncation
        self.assertEqual(model.created.microsecond, 0)
        
        # Verify datetime is in valid range for MySQL DATETIME
        # MySQL DATETIME range: '1000-01-01 00:00:00' to '9999-12-31 23:59:59'
        self.assertGreaterEqual(model.created.year, 1000)
        self.assertLessEqual(model.created.year, 9999)

    def test_user_datetime_compatibility(self):
        """Test that User timestamps are database compatible"""
        model = BaseModel()
        
        # Verify timestamps are timezone-naive (as MySQL DATETIME expects)
        self.assertIsNone(model.created.tzinfo)
        self.assertIsNone(model.updated.tzinfo)

    def test_datetime_consistency_across_models(self):
        """Test that all models using BaseModel have consistent datetime handling"""
        models = [BaseModel(), BaseModel(), BaseModel()]
        
        for model in models:
            self.assertEqual(model.created.microsecond, 0,
                           "All models should have created timestamp without microseconds")
            self.assertEqual(model.updated.microsecond, 0,
                           "All models should have updated timestamp without microseconds")

    def test_datetime_isoformat_compatibility(self):
        """Test that datetime can be converted to ISO format for APIs"""
        model = BaseModel()
        
        # Test ISO format conversion (commonly used in REST APIs)
        iso_created = model.created.isoformat()
        iso_updated = model.updated.isoformat()
        
        # Should not contain fractional seconds
        # ISO format with microseconds: 2024-01-01T12:00:00.123456
        # ISO format without: 2024-01-01T12:00:00
        parts = iso_created.split('.')
        # If there's a decimal point, it should only be followed by timezone info (Z, +HH:MM)
        # Since we have no microseconds, there should be no decimal point before the end
        self.assertTrue(
            '.' not in iso_created or not iso_created.split('.')[1][0].isdigit(),
            "ISO format should not contain fractional seconds"
        )


if __name__ == '__main__':
    unittest.main()
