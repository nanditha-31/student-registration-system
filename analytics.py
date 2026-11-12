"""
analytics.py
Creates simple Business Intelligence summaries from student records.
"""


def generate_report(students, total_processed=None, rejected_count=None):
    """Print data-quality, phone-prefix and email-domain summaries."""
    valid_count = len(students)

    if total_processed is None:
        total_processed = valid_count
    if rejected_count is None:
        rejected_count = max(total_processed - valid_count, 0)

    acceptance_rate = (
        (valid_count / total_processed) * 100 if total_processed else 0
    )

    phone_prefixes = {"6": 0, "7": 0, "8": 0, "9": 0}
    email_domains = {}

    for student in students:
        phone = student.get("phone", "")
        email = student.get("email", "")

        if phone and phone[0] in phone_prefixes:
            phone_prefixes[phone[0]] += 1

        domain = email.split("@")[-1].lower() if "@" in email else "unknown"
        email_domains[domain] = email_domains.get(domain, 0) + 1

    print("\n========== STUDENT REGISTRATION BI REPORT ==========")
    print(f"Total contacts processed : {total_processed}")
    print(f"Accepted registrations   : {valid_count}")
    print(f"Rejected records         : {rejected_count}")
    print(f"Acceptance rate           : {acceptance_rate:.2f}%")

    print("\nPHONE PREFIX DISTRIBUTION")
    for prefix in ["9", "8", "7", "6"]:
        print(f"{prefix}-series : {phone_prefixes[prefix]}")

    print("\nEMAIL DOMAIN DISTRIBUTION")
    if email_domains:
        for domain, count in sorted(email_domains.items()):
            print(f"{domain}: {count}")
    else:
        print("No email records available.")

    print("====================================================\n")
