
import json
import os
import tempfile
from decimal import Decimal
from pathlib import Path

from validator import (
    validate_item_name,
    validate_category,
    validate_quantity,
    validate_unit,
    validate_expiry_date,
    validate_threshold,
)


DEFAULT_STORAGE_PATH = Path("data/inventory.json")


class StorageError(Exception):
    """Raised when inventory storage operations fail."""


def validate_inventory_data(data):
    """Validate inventory data before saving or loading."""

    if not isinstance(data, dict):
        raise ValueError("Inventory data must be a dictionary.")

    validated = {}

    if len(data) > 10000:
        raise ValueError("Inventory contains too many items.")

    for item_id, item in data.items():

        if not isinstance(item_id, str):
            raise ValueError("Invalid inventory item identifier.")

        if not isinstance(item, dict):
            raise ValueError("Invalid inventory item.")

        required_fields = {
            "name",
            "category",
            "quantity",
            "unit",
            "expiry_date",
            "low_stock_threshold",
        }

        if set(item) != required_fields:
            raise ValueError("Inventory item has invalid fields.")

        name = validate_item_name(item["name"])

        if item_id != name.lower():
            raise ValueError("Inventory item identifier mismatch.")

        category = validate_category(item["category"])
        quantity = validate_quantity(item["quantity"])
        unit = validate_unit(item["unit"])
        threshold = validate_threshold(
            item["low_stock_threshold"]
        )

        expiry_date = item["expiry_date"]

        if expiry_date is not None:
            expiry_date = validate_expiry_date(
                expiry_date
            ).isoformat()

        validated[item_id] = {
            "name": name,
            "category": category,
            "quantity": quantity,
            "unit": unit,
            "expiry_date": expiry_date,
            "low_stock_threshold": threshold,
        }

    return validated


def save_inventory(inventory, filepath=DEFAULT_STORAGE_PATH):
    """Save inventory safely using an atomic file replacement."""

    if not isinstance(inventory, dict):
        raise TypeError("Inventory must be a dictionary.")

    validated = validate_inventory_data(inventory)

    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    serializable = {}

    for item_id, item in validated.items():
        serializable[item_id] = {
            **item,
            "quantity": str(item["quantity"]),
            "low_stock_threshold": str(
                item["low_stock_threshold"]
            ),
        }

    temporary_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:

            temporary_path = Path(temporary_file.name)

            json.dump(
                serializable,
                temporary_file,
                indent=4,
                allow_nan=False,
            )

            temporary_file.flush()
            os.fsync(temporary_file.fileno())

        os.replace(temporary_path, path)

    except (OSError, TypeError, ValueError) as error:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)

        raise StorageError(
            "Could not save inventory data."
        ) from error

    return path


def load_inventory(filepath=DEFAULT_STORAGE_PATH):
    """Load and validate inventory data."""

    path = Path(filepath)

    if not path.exists():
        return {}

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        validated = validate_inventory_data(data)

        return validated

    except (OSError, json.JSONDecodeError, ValueError, TypeError) as error:
        raise StorageError(
            "Could not load valid inventory data."
        ) from error
