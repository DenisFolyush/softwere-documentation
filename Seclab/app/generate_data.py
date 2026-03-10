"""Utility to generate a CSV file with dummy ticket data.

Usage:
    python -m app.generate_data output.csv 1000

If the count argument is omitted, 1000 rows will be produced by default.
"""
import csv
import random
import sys
from pathlib import Path

STATUS_CHOICES = ["new", "in_progress", "closed", "resolved"]


def generate_row(index: int):
    return {
        "title": f"Ticket {index}",
        "description": f"This is the description for ticket {index}.",
        "status": random.choice(STATUS_CHOICES),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m app.generate_data <output.csv> [count]")
        sys.exit(1)

    output = Path(sys.argv[1])
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 1000

    with output.open("w", newline='', encoding="utf-8") as csvfile:
        fieldnames = ["title", "description", "status"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(1, count + 1):
            writer.writerow(generate_row(i))

    print(f"Created {output} with {count} rows.")


if __name__ == "__main__":
    main()
