
import unittest
from datetime import date
from decimal import Decimal

from validator import (
    validate_item_name,
    validate_category,
    validate_quantity,
    validate_unit,
    validate_date,
    validate_expiry_date,
    validate_threshold,
)


class TestValidator(unittest.TestCase):

    def test_valid_item_name(self):
        self.assertEqual(
            validate_item_name(" Rice "),
            "Rice",
        )

    def test_empty_item_name(self):
        with self.assertRaises(ValueError):
            validate_item_name(" ")

    def test_invalid_item_name_characters(self):
        with self.assertRaises(ValueError):
            validate_item_name("../secret")

    def test_valid_category(self):
        self.assertEqual(
            validate_category("vegetables"),
            "Vegetables",
        )

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            validate_category("Electronics")

    def test_valid_quantity(self):
        self.assertEqual(
            validate_quantity("2.5"),
            Decimal("2.5"),
        )

    def test_negative_quantity(self):
        with self.assertRaises(ValueError):
            validate_quantity("-2")

    def test_zero_quantity(self):
        with self.assertRaises(ValueError):
            validate_quantity("0")

    def test_valid_unit(self):
        self.assertEqual(validate_unit("KG"), "kg")

    def test_invalid_unit(self):
        with self.assertRaises(ValueError):
            validate_unit("unknown")

    def test_valid_date(self):
        self.assertEqual(
            validate_date("2026-12-01"),
            date(2026, 12, 1),
        )

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            validate_date("01-12-2026")

    def test_valid_expiry_date(self):
        self.assertEqual(
            validate_expiry_date("2026-12-31"),
            date(2026, 12, 31),
        )

    def test_valid_threshold(self):
        self.assertEqual(
            validate_threshold("2"),
            Decimal("2"),
        )

    def test_negative_threshold(self):
        with self.assertRaises(ValueError):
            validate_threshold("-1")


if __name__ == "__main__":
    unittest.main()
