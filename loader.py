"""
loader.py
Reads contacts.csv, validates records, rejects duplicates and writes
accepted records to students_clean.csv.
"""

import csv
from pathlib import Path
from validator import validate_contact

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "contacts.csv"
CLEAN_FILE = BASE_DIR / "students_clean.csv"


def load_contacts(input_file=INPUT_FILE, output_file=CLEAN_FILE):
    """Load, validate and de-duplicate records. Return accepted records."""
    accepted = []
    seen_phones = set()
    seen_emails = set()
    rejected = []
    total = 0

    if not Path(input_file).exists():
        print(f"ERROR: Input file not found: {input_file}")
        print("Create contacts.csv in the same folder as main.py.")
        return accepted

    with open(input_file, "r", newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.DictReader(csv_file)

        required_columns = {"name", "phone", "email"}
        if not reader.fieldnames or not required_columns.issubset(
            set(reader.fieldnames)
        ):
            raise ValueError(
                "CSV must have these column headings: name,phone,email"
            )

        for row_number, row in enumerate(reader, start=2):
            total += 1
            name = (row.get("name") or "").strip()
            phone = (row.get("phone") or "").strip()
            email = (row.get("email") or "").strip()
            valid, reason = validate_contact(name, phone, email)

            if not valid:
                rejected.append((row_number, name, reason))
                continue

            phone_key = phone
            email_key = email.lower()

            if phone_key in seen_phones:
                rejected.append((row_number, name, "Duplicate phone number"))
                continue

            if email_key in seen_emails:
                rejected.append((row_number, name, "Duplicate email address"))
                continue

            seen_phones.add(phone_key)
            seen_emails.add(email_key)
            accepted.append({
                "name": name,
                "phone": phone,
                "email": email
            })

    with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["name", "phone", "email"])
        writer.writeheader()
        writer.writerows(accepted)

    print("\n========== CSV PROCESSING SUMMARY ==========")
    print(f"Total records read : {total}")
    print(f"Accepted records   : {len(accepted)}")
    print(f"Rejected records   : {len(rejected)}")

    if rejected:
        print("\nRejected records and reasons:")
        for row_number, name, reason in rejected:
            display_name = name if name else "(blank name)"
            print(f"CSV row {row_number} - {display_name}: {reason}")

    print(f"\nClean records saved to: {output_file}")
    return accepted


def save_contacts(contacts, output_file=CLEAN_FILE):
    """Save the current student list to the clean CSV file."""
    with open(output_file, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["name", "phone", "email"])
        writer.writeheader()
        writer.writerows(contacts)
