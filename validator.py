
import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation


def validate_item_name(value):
    """Validate and clean a kitchen inventory item name."""

    if not isinstance(value, str):
        raise TypeError("Item name must be text.")

    name = value.strip()

    if not name:
        raise ValueError("Item name cannot be empty.")

    if len(name) > 100:
        raise ValueError("Item name cannot exceed 100 characters.")

    if not re.fullmatch(r"[\w\s.,'()&-]+", name, flags=re.UNICODE):
        raise ValueError("Item name contains invalid characters.")

    return name


def validate_category(value):
    """Validate an inventory category."""

    if not isinstance(value, str):
        raise TypeError("Category must be text.")

    category = value.strip().title()

    allowed_categories = {
        "Vegetables",
        "Fruits",
        "Dairy",
        "Meat",
        "Seafood",
        "Grains",
        "Beverages",
        "Spices",
        "Canned Goods",
        "Snacks",
        "Other",
    }

    if category not in allowed_categories:
        raise ValueError("Invalid inventory category.")

    return category


def validate_quantity(value):
    """Validate a positive inventory quantity."""

    if isinstance(value, bool):
        raise TypeError("Quantity must be a number.")

    try:
        quantity = Decimal(str(value).strip())
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Enter a valid quantity.")

    if not quantity.is_finite():
        raise ValueError("Quantity must be finite.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    if quantity > Decimal("1000000"):
        raise ValueError("Quantity exceeds the allowed limit.")

    return quantity


def validate_unit(value):
    """Validate the measurement unit."""

    if not isinstance(value, str):
        raise TypeError("Unit must be text.")

    unit = value.strip().lower()

    allowed_units = {
        "kg",
        "g",
        "litre",
        "ml",
        "pieces",
        "packets",
        "bottles",
        "cans",
        "boxes",
    }

    if unit not in allowed_units:
        raise ValueError("Invalid measurement unit.")

    return unit


def validate_date(value, field_name="Date"):
    """Validate a date in YYYY-MM-DD format."""

    if isinstance(value, datetime):
        raise TypeError(f"{field_name} must be a date, not a datetime.")

    if isinstance(value, date):
        return value

    if not isinstance(value, str):
        raise TypeError(f"{field_name} must be text.")

    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError:
        raise ValueError(
            f"{field_name} must use YYYY-MM-DD format."
        )


def validate_expiry_date(value):
    """Validate an expiry date."""

    expiry_date = validate_date(value, "Expiry date")

    return expiry_date


def validate_threshold(value):
    """Validate a non-negative low-stock threshold."""

    if isinstance(value, bool):
        raise TypeError("Threshold must be a number.")

    try:
        threshold = Decimal(str(value).strip())
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Enter a valid threshold.")

    if not threshold.is_finite() or threshold < 0:
        raise ValueError("Threshold must be finite and non-negative.")

    if threshold > Decimal("1000000"):
        raise ValueError("Threshold exceeds the allowed limit.")

    return threshold
