
import unittest
from datetime import date, timedelta
from decimal import Decimal

from inventory import Inventory


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.inventory = Inventory()

        self.inventory.add_item(
            name="Rice",
            category="Grains",
            quantity=10,
            unit="kg",
            low_stock_threshold=2,
        )

    def test_add_item(self):
        self.assertEqual(len(self.inventory.items), 1)

    def test_prevent_duplicate_item(self):
        with self.assertRaises(ValueError):
            self.inventory.add_item(
                "Rice", "Grains", 5, "kg"
            )

    def test_update_quantity(self):
        self.inventory.update_quantity("Rice", 15)

        self.assertEqual(
            self.inventory.items["rice"]["quantity"],
            Decimal("15"),
        )

    def test_consume_item(self):
        remaining = self.inventory.consume_item("Rice", 3)

        self.assertEqual(remaining, Decimal("7"))

    def test_prevent_overconsumption(self):
        with self.assertRaises(ValueError):
            self.inventory.consume_item("Rice", 20)

    def test_restock_item(self):
        new_quantity = self.inventory.restock_item("Rice", 5)

        self.assertEqual(new_quantity, Decimal("15"))

    def test_remove_item(self):
        self.inventory.remove_item("Rice")

        self.assertEqual(len(self.inventory.items), 0)

    def test_search_items(self):
        results = self.inventory.search_items("ric")

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Rice")

    def test_low_stock_detection(self):
        self.inventory.update_quantity("Rice", 2)

        self.assertEqual(
            len(self.inventory.get_low_stock_items()),
            1,
        )

    def test_expired_item_detection(self):
        self.inventory.add_item(
            "Old Milk",
            "Dairy",
            2,
            "litre",
            expiry_date=date.today() - timedelta(days=1),
        )

        self.assertEqual(
            len(self.inventory.get_expired_items()),
            1,
        )

    def test_expiring_soon_detection(self):
        self.inventory.add_item(
            "Fresh Milk",
            "Dairy",
            2,
            "litre",
            expiry_date=date.today() + timedelta(days=3),
        )

        self.assertEqual(
            len(self.inventory.get_expiring_soon_items()),
            1,
        )

    def test_missing_item(self):
        with self.assertRaises(ValueError):
            self.inventory.remove_item("Sugar")


if __name__ == "__main__":
    unittest.main()
