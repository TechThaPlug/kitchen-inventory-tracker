
import tempfile
import unittest

from pathlib import Path
from decimal import Decimal

from reports import (
    generate_inventory_report,
    generate_stock_alert_report,
    save_report,
)


class TestReports(unittest.TestCase):

    def setUp(self):
        self.items = [
            {
                "name": "Rice",
                "category": "Grains",
                "quantity": Decimal("10"),
                "unit": "kg",
                "expiry_date": None,
                "low_stock_threshold": Decimal("2"),
            },
            {
                "name": "Milk",
                "category": "Dairy",
                "quantity": Decimal("1"),
                "unit": "litre",
                "expiry_date": "2026-12-01",
                "low_stock_threshold": Decimal("2"),
            },
        ]

        self.temp_directory = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_directory.cleanup()

    def test_generate_inventory_report(self):
        report = generate_inventory_report(self.items)

        self.assertIn("Rice", report)
        self.assertIn("Milk", report)
        self.assertIn("CATEGORY SUMMARY", report)

    def test_empty_inventory_report(self):
        report = generate_inventory_report([])

        self.assertIn("No inventory items available.", report)

    def test_generate_stock_alert_report(self):
        report = generate_stock_alert_report([self.items[1]])

        self.assertIn("LOW STOCK ALERT", report)
        self.assertIn("Milk", report)

    def test_empty_stock_alert_report(self):
        report = generate_stock_alert_report([])

        self.assertIn("No low-stock items", report)

    def test_save_report(self):
        saved_path = save_report(
            "Kitchen inventory report",
            "inventory_report.txt",
            self.temp_directory.name,
        )

        self.assertTrue(saved_path.exists())

    def test_prevent_report_overwriting(self):
        save_report(
            "First report",
            "inventory_report.txt",
            self.temp_directory.name,
        )

        with self.assertRaises(FileExistsError):
            save_report(
                "Second report",
                "inventory_report.txt",
                self.temp_directory.name,
            )

    def test_prevent_path_traversal(self):
        with self.assertRaises(ValueError):
            save_report(
                "Test report",
                "../malicious.txt",
                self.temp_directory.name,
            )

    def test_reject_invalid_inventory_record(self):
        with self.assertRaises(ValueError):
            generate_inventory_report([{"name": "Rice"}])

    def test_reject_negative_quantity(self):
        invalid_items = [self.items[0].copy()]
        invalid_items[0]["quantity"] = Decimal("-5")

        with self.assertRaises(ValueError):
            generate_inventory_report(invalid_items)

    def test_reject_boolean_quantity(self):
        invalid_items = [self.items[0].copy()]
        invalid_items[0]["quantity"] = True

        with self.assertRaises(ValueError):
            generate_inventory_report(invalid_items)

    def test_reject_non_finite_quantity(self):
        invalid_items = [self.items[0].copy()]
        invalid_items[0]["quantity"] = Decimal("NaN")

        with self.assertRaises(ValueError):
            generate_inventory_report(invalid_items)


if __name__ == "__main__":
    unittest.main()
