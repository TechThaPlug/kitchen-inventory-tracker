# Kitchen Inventory Tracker

A secure, command-line Python application for managing kitchen inventory, monitoring stock levels, tracking expiry dates, and generating inventory reports.

## Features

- Add, update, restock, and remove inventory items.
- Record consumed quantities.
- Search inventory by item name.
- Categorize kitchen supplies.
- Track expiry dates.
- Detect expired and soon-to-expire items.
- Generate inventory and low-stock reports.
- Persist inventory data using JSON.
- Validate user input and stored data.
- Save reports safely without overwriting existing files.

## Technologies

- Python 3.13+
- JSON
- Decimal precision
- Python unittest

## Project Structure

```text
kitchen-inventory-tracker/
├── data/
├── reports/
├── tests/
├── inventory.py
├── validator.py
├── storage.py
├── reports.py
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/TechThaPlug/kitchen-inventory-tracker.git
```

Enter the project directory:

```bash
cd kitchen-inventory-tracker
```

Create a virtual environment:

```bash
py -3.13 -m venv .venv
```

Activate it on Windows:

```cmd
.venv\Scripts\activate
```

No third-party dependencies are required.

## Run the Application

```bash
python main.py
```

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Compile Check

```bash
python -m compileall -q .
```

## Data Storage

Inventory records are stored locally in:

```text
data/inventory.json
```

Generated reports are saved in:

```text
reports/
```

## Security and Reliability

- Input validation for inventory records.
- Strict validation of stored JSON data.
- Decimal-based quantity handling.
- Atomic inventory file replacement.
- Report filename validation.
- Protection against report filename path traversal.
- Automated unit tests.

## Author

**Anthony W. Maina**

GitHub: [TechThaPlug](https://github.com/TechThaPlug)

## License

MIT License
