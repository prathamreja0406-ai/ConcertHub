
from datetime import datetime


def validate_name(name):
    if not name or not name.strip():
        raise ValueError("Name cannot be empty.")

    if len(name.strip()) < 2:
        raise ValueError("Name must contain at least 2 characters.")

    return name.strip()


def validate_email(email):
    email = email.strip().lower()

    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Please enter a valid email address.")

    return email


def validate_password(password):
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")

    return password


def validate_positive_integer(value, field_name):
    try:
        value = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid integer.")

    if value <= 0:
        raise ValueError(f"{field_name} must be greater than zero.")

    return value


def validate_non_negative_number(value, field_name):
    try:
        value = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid number.")

    if value < 0:
        raise ValueError(f"{field_name} cannot be negative.")

    return value


def validate_date(date_text):
    try:
        date_value = datetime.strptime(date_text, "%Y-%m-%d")
        return date_value.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError(
            "Date must be in YYYY-MM-DD format."
        )


def validate_future_date(date_text):
    date_text = validate_date(date_text)

    concert_date = datetime.strptime(
        date_text, "%Y-%m-%d"
    ).date()

    if concert_date <= datetime.now().date():
        raise ValueError(
            "Concert date must be in the future."
        )

    return date_text


def validate_ticket_type(ticket_type):
    ticket_type = ticket_type.strip().lower()

    allowed_types = {
        "regular",
        "vip",
        "premium"
    }

    if ticket_type not in allowed_types:
        raise ValueError(
            "Ticket type must be Regular, VIP, or Premium."
        )

    return ticket_type
