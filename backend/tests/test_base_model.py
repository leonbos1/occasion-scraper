import unittest
import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.base import BaseModel


class TestBaseModelDatetimeHandling(unittest.TestCase):
    """Test BaseModel datetime creation without microseconds"""

    def test_created_timestamp_has_no_microseconds(self):
        """Test that created timestamp is set without microseconds"""
        model = BaseModel()
        self.assertEqual(model.created.microsecond, 0, 
                        "created timestamp should have no microseconds")

    def test_updated_timestamp_has_no_microseconds(self):
        """Test that updated timestamp is set without microseconds"""
        model = BaseModel()
        self.assertEqual(model.updated.microsecond, 0,
                        "updated timestamp should have no microseconds")

    def test_created_and_updated_are_equal_on_creation(self):
        """Test that created and updated timestamps are identical on creation"""
        model = BaseModel()
        self.assertEqual(model.created, model.updated,
                        "created and updated should be identical on creation")

    def test_id_is_generated_when_not_provided(self):
        """Test that id is auto-generated as UUID when not provided"""
        model = BaseModel()
        self.assertIsNotNone(model.id)
        self.assertEqual(len(model.id), 36)  # UUID4 string format length

    def test_id_is_used_when_provided(self):
        """Test that provided id is used instead of generating new one"""
        custom_id = "test-id-12345"
        model = BaseModel(id=custom_id)
        self.assertEqual(model.id, custom_id)

    def test_timestamps_are_datetime_objects(self):
        """Test that created and updated are datetime objects"""
        model = BaseModel()
        self.assertIsInstance(model.created, datetime.datetime)
        self.assertIsInstance(model.updated, datetime.datetime)

    def test_timestamp_format_compatibility(self):
        """Test that timestamps can be converted to string without fractional seconds"""
        model = BaseModel()
        created_str = str(model.created).split('.')[0]
        # Should have format: YYYY-MM-DD HH:MM:SS
        self.assertEqual(len(created_str), 19)
        self.assertIn('-', created_str)
        self.assertIn(':', created_str)
        self.assertIn(' ', created_str)


if __name__ == '__main__':
    unittest.main()
