
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
import re


def generate_inventory_report(items):
    """Generate a professional kitchen inventory report."""

    if not isinstance(items, list):
        raise TypeError("Inventory items must be a list.")

    lines = [
        "=" * 65,
        "                 KITCHEN INVENTORY TRACKER",
        "                     INVENTORY REPORT",
        "=" * 65,
        f"Generated: {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}",
        f"Total unique items: {len(items)}",
        "=" * 65,
        "",
        "INVENTORY DETAILS",
        "-" * 65,
    ]

    if not items:
        lines.append("No inventory items available.")

    required_fields = {
        "name",
        "category",
        "quantity",
        "unit",
        "expiry_date",
        "low_stock_threshold",
    }

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Invalid inventory record.")

        if set(item) != required_fields:
            raise ValueError("Inventory record has invalid fields.")

        name = item["name"]
        category = item["category"]
        quantity = item["quantity"]
        unit = item["unit"]
        expiry_date = item["expiry_date"]
        threshold = item["low_stock_threshold"]

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Invalid item name.")

        if not isinstance(category, str) or not category.strip():
            raise ValueError("Invalid item category.")

        if not isinstance(unit, str) or not unit.strip():
            raise ValueError("Invalid measurement unit.")

        if isinstance(quantity, bool) or not isinstance(
            quantity, (int, float, Decimal)
        ):
            raise ValueError("Invalid inventory quantity.")

        if not Decimal(str(quantity)).is_finite():
            raise ValueError("Inventory quantity must be finite.")

        if quantity <= 0:
            raise ValueError("Inventory quantity must be positive.")

        if isinstance(threshold, bool) or not isinstance(
            threshold, (int, float, Decimal)
        ):
            raise ValueError("Invalid low-stock threshold.")

        if not Decimal(str(threshold)).is_finite() or threshold < 0:
            raise ValueError("Invalid low-stock threshold.")

        if expiry_date is not None and not isinstance(
            expiry_date, str
        ):
            raise ValueError("Invalid expiry date.")

        lines.extend([
            f"Item: {name}",
            f"Category: {category}",
            f"Quantity: {quantity} {unit}",
            f"Expiry date: {expiry_date or 'Not specified'}",
            f"Low-stock threshold: {threshold} {unit}",
            "-" * 65,
        ])

    lines.extend([
        "",
        "CATEGORY SUMMARY",
        "-" * 65,
    ])

    category_counts = {}

    for item in items:
        category = item["category"]
        category_counts[category] = (
            category_counts.get(category, 0) + 1
        )

    if category_counts:
        for category, count in sorted(category_counts.items()):
            lines.append(f"{category}: {count} item(s)")
    else:
        lines.append("No categories available.")

    lines.extend([
        "",
        "=" * 65,
        "              Keep your kitchen organized!",
        "=" * 65,
    ])

    return "\n".join(lines)


def generate_stock_alert_report(items):
    """Generate a report of items requiring restocking."""

    if not isinstance(items, list):
        raise TypeError("Items must be a list.")

    lines = [
        "=" * 65,
        "                    LOW STOCK ALERT",
        "=" * 65,
    ]

    if not items:
        lines.append("No low-stock items. Your inventory is healthy!")

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Invalid inventory record.")

        required_fields = {
            "name",
            "quantity",
            "unit",
            "low_stock_threshold",
        }

        if not required_fields.issubset(item):
            raise ValueError("Incomplete stock information.")

        lines.append(
            f"{item['name']}: {item['quantity']} "
            f"{item['unit']} remaining "
            f"(Threshold: {item['low_stock_threshold']})"
        )

    lines.append("=" * 65)

    return "\n".join(lines)


def save_report(report, filename, directory="reports"):
    """Save a report without allowing path traversal or overwriting."""

    if not isinstance(report, str) or not report.strip():
        raise ValueError("Report content cannot be empty.")

    if not isinstance(filename, str):
        raise TypeError("Filename must be text.")

    if (
        not filename.strip()
        or Path(filename).name != filename
        or filename in {".", ".."}
        or "/" in filename
        or "\\" in filename
    ):
        raise ValueError("Invalid report filename.")

    if not re.fullmatch(
        r"[a-zA-Z0-9_-]+\.txt",
        filename,
        flags=re.IGNORECASE,
    ):
        raise ValueError("Invalid report filename format.")

    report_directory = Path(directory).resolve()
    report_directory.mkdir(parents=True, exist_ok=True)

    destination = report_directory / filename

    with destination.open("x", encoding="utf-8") as file:
        file.write(report)

    return destination
