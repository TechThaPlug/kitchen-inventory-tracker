
from datetime import datetime
from pathlib import Path

from inventory import Inventory
from storage import load_inventory, save_inventory, StorageError
from reports import (
    generate_inventory_report,
    generate_stock_alert_report,
    save_report,
)
from validator import (
    validate_item_name,
    validate_category,
    validate_quantity,
    validate_unit,
    validate_expiry_date,
    validate_threshold,
)


def get_input(prompt, validator):
    """Request input until validation succeeds."""

    while True:
        try:
            return validator(input(prompt))

        except (ValueError, TypeError) as error:
            print(f"Error: {error}")


def get_optional_expiry_date():
    """Collect an optional expiry date."""

    while True:
        value = input(
            "Expiry date (YYYY-MM-DD) or press Enter to skip: "
        ).strip()

        if not value:
            return None

        try:
            return validate_expiry_date(value)

        except (ValueError, TypeError) as error:
            print(f"Error: {error}")


def display_items(items):
    """Display inventory records."""

    if not items:
        print("\nNo inventory items found.")
        return

    print("\n" + "=" * 65)
    print("                    KITCHEN INVENTORY")
    print("=" * 65)

    for number, item in enumerate(items, start=1):
        print(f"\n{number}. {item['name']}")
        print(f"   Category: {item['category']}")
        print(f"   Quantity: {item['quantity']} {item['unit']}")
        print(
            f"   Expiry: {item['expiry_date'] or 'Not specified'}"
        )
        print(
            f"   Low-stock threshold: "
            f"{item['low_stock_threshold']} {item['unit']}"
        )

    print("\n" + "=" * 65)


def add_item(inventory):
    """Add a kitchen item."""

    print("\n--- ADD KITCHEN ITEM ---")

    name = get_input("Item name: ", validate_item_name)

    category = get_input(
        "Category: ",
        validate_category,
    )

    quantity = get_input(
        "Quantity: ",
        validate_quantity,
    )

    unit = get_input(
        "Unit (kg, g, litre, ml, pieces, packets, bottles, cans, boxes): ",
        validate_unit,
    )

    expiry_date = get_optional_expiry_date()

    threshold = get_input(
        "Low-stock threshold: ",
        validate_threshold,
    )

    item = inventory.add_item(
        name=name,
        category=category,
        quantity=quantity,
        unit=unit,
        expiry_date=expiry_date,
        low_stock_threshold=threshold,
    )

    print(f"\nSuccessfully added {item['name']}!")


def restock_item(inventory):
    """Restock an existing item."""

    print("\n--- RESTOCK ITEM ---")

    name = input("Item name: ")

    quantity = get_input(
        "Additional quantity: ",
        validate_quantity,
    )

    new_quantity = inventory.restock_item(name, quantity)

    print(f"\nNew quantity: {new_quantity}")


def consume_item(inventory):
    """Record consumed food."""

    print("\n--- CONSUME ITEM ---")

    name = input("Item name: ")

    quantity = get_input(
        "Quantity consumed: ",
        validate_quantity,
    )

    remaining = inventory.consume_item(name, quantity)

    if remaining == 0:
        print("\nItem completely consumed and removed from inventory.")
    else:
        print(f"\nRemaining quantity: {remaining}")


def update_item(inventory):
    """Update an item's quantity."""

    print("\n--- UPDATE ITEM ---")

    name = input("Item name: ")

    quantity = get_input(
        "New total quantity: ",
        validate_quantity,
    )

    inventory.update_quantity(name, quantity)

    print("\nInventory quantity updated successfully!")


def remove_item(inventory):
    """Remove an item."""

    print("\n--- REMOVE ITEM ---")

    name = input("Item name: ")

    inventory.remove_item(name)

    print("\nItem removed successfully!")


def search_items(inventory):
    """Search for inventory items."""

    print("\n--- SEARCH INVENTORY ---")

    search_term = input("Search item name: ")

    results = inventory.search_items(search_term)

    display_items(results)


def show_alerts(inventory):
    """Display low-stock and expiry alerts."""

    print("\n--- INVENTORY ALERTS ---")

    low_stock = inventory.get_low_stock_items()
    expired = inventory.get_expired_items()
    expiring_soon = inventory.get_expiring_soon_items(7)

    print("\nLOW STOCK ITEMS")

    if low_stock:
        for item in low_stock:
            print(
                f"- {item['name']}: {item['quantity']} "
                f"{item['unit']} remaining"
            )
    else:
        print("No low-stock items.")

    print("\nEXPIRED ITEMS")

    if expired:
        for item in expired:
            print(f"- {item['name']} (Expired: {item['expiry_date']})")
    else:
        print("No expired items.")

    print("\nEXPIRING WITHIN 7 DAYS")

    if expiring_soon:
        for item in expiring_soon:
            print(f"- {item['name']} (Expires: {item['expiry_date']})")
    else:
        print("No items expiring soon.")


def generate_reports(inventory):
    """Generate and save inventory reports."""

    print("\n--- GENERATE REPORT ---")

    report_type = input(
        "Choose report (1: Full inventory, 2: Low stock): "
    ).strip()

    if report_type == "1":
        report = generate_inventory_report(
            inventory.get_all_items()
        )

        filename_prefix = "inventory_report"

    elif report_type == "2":
        report = generate_stock_alert_report(
            inventory.get_low_stock_items()
        )

        filename_prefix = "low_stock_report"

    else:
        print("Invalid report selection.")
        return

    print("\n" + report)

    save_choice = input(
        "\nSave this report? (y/n): "
    ).strip().lower()

    if save_choice == "y":
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")

        filename = f"{filename_prefix}_{timestamp}.txt"

        saved_path = save_report(
            report,
            filename,
        )

        print(f"\nReport saved: {saved_path}")


def display_menu():
    """Display the main application menu."""

    print("\n" + "=" * 65)
    print("                 KITCHEN INVENTORY TRACKER")
    print("=" * 65)
    print("1. Add kitchen item")
    print("2. View all inventory")
    print("3. Update item quantity")
    print("4. Restock item")
    print("5. Consume item")
    print("6. Remove item")
    print("7. Search inventory")
    print("8. View inventory alerts")
    print("9. Generate reports")
    print("0. Save and exit")
    print("=" * 65)


def run_application():
    """Start the kitchen inventory application."""

    inventory = Inventory()

    try:
        inventory.items = load_inventory()

    except StorageError as error:
        print(f"\nStorage error: {error}")
        print("Please check your inventory data before continuing.")
        return

    print("\nWelcome to Kitchen Inventory Tracker!")

    actions = {
        "1": add_item,
        "2": lambda inv: display_items(inv.get_all_items()),
        "3": update_item,
        "4": restock_item,
        "5": consume_item,
        "6": remove_item,
        "7": search_items,
        "8": show_alerts,
        "9": generate_reports,
    }

    while True:
        display_menu()

        choice = input("Choose an option: ").strip()

        if choice == "0":
            try:
                save_inventory(inventory.items)

                print("\nInventory saved successfully!")
                print("Thank you for using Kitchen Inventory Tracker!")

            except StorageError as error:
                print(f"\nCould not save inventory: {error}")

            break

        action = actions.get(choice)

        if action is None:
            print("\nInvalid option. Please choose 0 to 9.")
            continue

        try:
            action(inventory)
            save_inventory(inventory.items)

        except (ValueError, TypeError) as error:
            print(f"\nError: {error}")

        except (StorageError, OSError) as error:
            print(f"\nStorage error: {error}")


if __name__ == "__main__":
    try:
        run_application()

    except KeyboardInterrupt:
        print("\n\nApplication interrupted.")
