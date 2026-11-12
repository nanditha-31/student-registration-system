"""
validator.py
Validates student name, phone number and email address.
"""


def validate_name(name):
    """Return (is_valid, message) for a student's name."""
    if name is None or not name.strip():
        return False, "Name is missing"
    if any(char.isdigit() for char in name):
        return False, "Name must not contain numbers"
    return True, "Valid name"


def validate_phone(phone):
    """Phone must contain exactly 10 digits and start with 6, 7, 8 or 9."""
    if phone is None or not phone.strip():
        return False, "Phone number is missing"

    phone = phone.strip()

    if not phone.isdigit():
        return False, "Phone number must contain digits only"
    if len(phone) != 10:
        return False, "Phone number must contain exactly 10 digits"
    if phone[0] not in "6789":
        return False, "Phone number must start with 6, 7, 8 or 9"

    return True, "Valid phone number"


def validate_email(email):
    """A simple practical email check for this beginner project."""
    if email is None or not email.strip():
        return False, "Email address is missing"

    email = email.strip()

    if " " in email:
        return False, "Email must not contain spaces"
    if email.count("@") != 1:
        return False, "Email must contain exactly one @ symbol"

    local, domain = email.split("@")

    if not local:
        return False, "Email must contain text before @"
    if not domain or "." not in domain:
        return False, "Email domain must contain a dot"
    if domain.startswith(".") or domain.endswith("."):
        return False, "Email domain cannot start or end with a dot"
    if ".." in email:
        return False, "Email must not contain consecutive dots"

    return True, "Valid email address"


def validate_contact(name, phone, email):
    """
    Validate all three fields.
    Returns (True, 'Valid contact') or (False, reason).
    """
    checks = [
        validate_name(name),
        validate_phone(phone),
        validate_email(email),
    ]

    errors = [message for is_valid, message in checks if not is_valid]

    if errors:
        return False, "; ".join(errors)

    return True, "Valid contact"
