
import json
import tempfile
import unittest

from pathlib import Path
from decimal import Decimal

from storage import (
    save_inventory,
    load_inventory,
    StorageError,
)


class TestStorage(unittest.TestCase):

    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()

        self.filepath = (
            Path(self.temp_directory.name) / "inventory.json"
        )

        self.sample_inventory = {
            "rice": {
                "name": "Rice",
                "category": "Grains",
                "quantity": Decimal("10"),
                "unit": "kg",
                "expiry_date": None,
                "low_stock_threshold": Decimal("2"),
            }
        }

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_save_inventory(self):
        save_inventory(
            self.sample_inventory,
            self.filepath,
        )

        self.assertTrue(self.filepath.exists())

    def test_load_inventory(self):
        save_inventory(
            self.sample_inventory,
            self.filepath,
        )

        loaded = load_inventory(self.filepath)

        self.assertEqual(
            loaded["rice"]["quantity"],
            Decimal("10"),
        )

    def test_missing_file_returns_empty_inventory(self):
        loaded = load_inventory(self.filepath)

        self.assertEqual(loaded, {})

    def test_invalid_json(self):
        self.filepath.write_text(
            "{invalid json",
            encoding="utf-8",
        )

        with self.assertRaises(StorageError):
            load_inventory(self.filepath)

    def test_invalid_inventory_data(self):
        self.filepath.write_text(
            json.dumps({"rice": {"name": "Rice"}}),
            encoding="utf-8",
        )

        with self.assertRaises(StorageError):
            load_inventory(self.filepath)

    def test_invalid_inventory_cannot_be_saved(self):
        invalid_inventory = {
            "rice": {
                "name": "Rice",
                "category": "Grains",
                "quantity": Decimal("-5"),
                "unit": "kg",
                "expiry_date": None,
                "low_stock_threshold": Decimal("2"),
            }
        }

        with self.assertRaises(ValueError):
            save_inventory(
                invalid_inventory,
                self.filepath,
            )


if __name__ == "__main__":
    unittest.main()
