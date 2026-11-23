
from datetime import date
from decimal import Decimal

from validator import (
    validate_item_name,
    validate_category,
    validate_quantity,
    validate_unit,
    validate_expiry_date,
    validate_threshold,
)


class Inventory:
    """Manage kitchen inventory records."""

    def __init__(self):
        self.items = {}

    def add_item(
        self,
        name,
        category,
        quantity,
        unit,
        expiry_date=None,
        low_stock_threshold=1,
    ):
        """Add a new item to inventory."""

        name = validate_item_name(name)
        category = validate_category(category)
        quantity = validate_quantity(quantity)
        unit = validate_unit(unit)
        threshold = validate_threshold(low_stock_threshold)

        if expiry_date is not None:
            expiry_date = validate_expiry_date(expiry_date)

        item_id = name.lower()

        if item_id in self.items:
            raise ValueError("This item already exists.")

        self.items[item_id] = {
            "name": name,
            "category": category,
            "quantity": quantity,
            "unit": unit,
            "expiry_date": (
                expiry_date.isoformat()
                if expiry_date else None
            ),
            "low_stock_threshold": threshold,
        }

        return self.items[item_id]

    def update_quantity(self, name, quantity):
        """Set an item's current quantity."""

        item_id = self._get_item_id(name)
        new_quantity = validate_quantity(quantity)

        self.items[item_id]["quantity"] = new_quantity

        return self.items[item_id]

    def consume_item(self, name, quantity):
        """Record consumption of an inventory item."""

        item_id = self._get_item_id(name)
        consumed_quantity = validate_quantity(quantity)

        current_quantity = self.items[item_id]["quantity"]

        if consumed_quantity > current_quantity:
            raise ValueError("Insufficient stock available.")

        remaining = current_quantity - consumed_quantity

        if remaining == 0:
            del self.items[item_id]
            return Decimal("0")

        self.items[item_id]["quantity"] = remaining

        return remaining

    def restock_item(self, name, quantity):
        """Increase an item's available quantity."""

        item_id = self._get_item_id(name)
        additional_quantity = validate_quantity(quantity)

        current_quantity = self.items[item_id]["quantity"]
        new_quantity = current_quantity + additional_quantity

        self.items[item_id]["quantity"] = validate_quantity(
            new_quantity
        )

        return new_quantity

    def remove_item(self, name):
        """Remove an item from inventory."""

        item_id = self._get_item_id(name)

        return self.items.pop(item_id)

    def search_items(self, search_term):
        """Search inventory by item name."""

        if not isinstance(search_term, str):
            raise TypeError("Search term must be text.")

        term = search_term.strip().casefold()

        if not term:
            raise ValueError("Search term cannot be empty.")

        return [
            item.copy()
            for item in self.items.values()
            if term in item["name"].casefold()
        ]

    def get_all_items(self):
        """Return all inventory items."""

        return [
            item.copy()
            for item in self.items.values()
        ]

    def get_low_stock_items(self):
        """Find items at or below their low-stock threshold."""

        return [
            item.copy()
            for item in self.items.values()
            if item["quantity"] <= item["low_stock_threshold"]
        ]

    def get_expired_items(self):
        """Find items whose expiry dates have passed."""

        today = date.today()

        return [
            item.copy()
            for item in self.items.values()
            if item["expiry_date"]
            and date.fromisoformat(item["expiry_date"]) < today
        ]

    def get_expiring_soon_items(self, days=7):
        """Find items expiring within the next specified days."""

        if isinstance(days, bool) or not isinstance(days, int):
            raise TypeError("Days must be an integer.")

        if not 0 <= days <= 365:
            raise ValueError("Days must be between 0 and 365.")

        today = date.today()

        return [
            item.copy()
            for item in self.items.values()
            if item["expiry_date"]
            and today <= date.fromisoformat(item["expiry_date"])
            <= date.fromordinal(today.toordinal() + days)
        ]

    def _get_item_id(self, name):
        """Find an existing item using its name."""

        name = validate_item_name(name)
        item_id = name.lower()

        if item_id not in self.items:
            raise ValueError(f"Item '{name}' was not found.")

        return item_id
