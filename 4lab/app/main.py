import argparse
import csv
import json
import sys
import urllib.request
from collections import Counter
from pathlib import Path

from app.output_strategy import build_strategy

API_URL = "https://data.cityofnewyork.us/resource/pvqr-7yc4.json"
DEFAULT_FIELDS = [
    "summons_number",
    "plate_id",
    "registration_state",
    "plate_type",
    "violation_code",
    "vehicle_body_type",
    "vehicle_make",
    "issuing_agency",
    "street_name",
    "house_number",
    "violation_precinct",
    "issuer_precinct",
    "law_section",
    "vehicle_color",
    "vehicle_year",
    "fiscal_year",
]


def fetch_records(limit):
    query = f"{API_URL}?$limit={limit}"
    with urllib.request.urlopen(query, timeout=30) as response:
        return json.load(response)


def save_json(records, path):
    with open(path, "w", encoding="utf-8") as stream:
        json.dump(records, stream, indent=2, ensure_ascii=False)


def save_csv(records, path, fields):
    with open(path, "w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for record in records:
            writer.writerow({k: record.get(k, "") for k in fields})


def print_summary(records, top_n=10):
    print("Fetched records:", len(records))
    if not records:
        return

    violation_codes = Counter(r.get("violation_code", "UNKNOWN") for r in records)
    street_names = Counter((r.get("street_name") or "UNKNOWN").upper() for r in records)
    vehicle_makes = Counter((r.get("vehicle_make") or "UNKNOWN").upper() for r in records)

    print("\nTop violation codes:")
    for code, count in violation_codes.most_common(top_n):
        print(f"  {code}: {count}")

    print("\nTop street names:")
    for street, count in street_names.most_common(top_n):
        print(f"  {street}: {count}")

    print("\nTop vehicle makes:")
    for make, count in vehicle_makes.most_common(top_n):
        print(f"  {make}: {count}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fetch variant 26 parking violations data from NYC Open Data."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=1000,
        help="Number of records to fetch from the API (default: 1000).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("parking_violations_2019.json"),
        help="Output file path for saved data.",
    )
    parser.add_argument(
        "--format",
        choices=["json", "csv"],
        default="json",
        help="Format to save fetched data.",
    )
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print a summary of the fetched records.",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("config.json"),
        help="Path to the output strategy configuration file.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    print(f"Fetching {args.limit} records from the NYC parking violations API...")

    try:
        records = fetch_records(args.limit)
    except Exception as exc:
        print("Error fetching data:", exc)
        sys.exit(1)

    if args.format == "json":
        output_path = args.output
    else:
        output_path = args.output.with_suffix(".csv")

    if args.format == "json":
        save_json(records, output_path)
    else:
        save_csv(records, output_path, DEFAULT_FIELDS)

    print(f"Saved {len(records)} records to {output_path}")

    try:
        writer = build_strategy(str(args.config))
        writer.write(records)
    except Exception as exc:
        print("Output strategy error:", exc)
        sys.exit(1)

    if args.summary:
        print_summary(records)


if __name__ == "__main__":
    main()
