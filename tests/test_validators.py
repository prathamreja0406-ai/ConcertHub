import unittest
from datetime import datetime, timedelta

from app.validators import (
    validate_name,
    validate_email,
    validate_password,
    validate_positive_integer,
    validate_non_negative_number,
    validate_date,
    validate_future_date,
    validate_ticket_type
)


class TestValidators(unittest.TestCase):

    def test_valid_name(self):
        self.assertEqual(validate_name("  Pratham  "), "Pratham")

    def test_invalid_name(self):
        with self.assertRaises(ValueError):
            validate_name("")

    def test_valid_email(self):
        self.assertEqual(
            validate_email("USER@Example.COM"),
            "user@example.com"
        )

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            validate_email("invalid-email")

    def test_valid_password(self):
        self.assertEqual(
            validate_password("Concert@123"),
            "Concert@123"
        )

    def test_short_password(self):
        with self.assertRaises(ValueError):
            validate_password("123")

    def test_positive_integer(self):
        self.assertEqual(
            validate_positive_integer("10", "Quantity"),
            10
        )

    def test_invalid_positive_integer(self):
        with self.assertRaises(ValueError):
            validate_positive_integer("0", "Quantity")

    def test_non_negative_number(self):
        self.assertEqual(
            validate_non_negative_number("99.50", "Price"),
            99.50
        )

    def test_negative_number(self):
        with self.assertRaises(ValueError):
            validate_non_negative_number("-10", "Price")

    def test_valid_date(self):
        self.assertEqual(
            validate_date("2026-12-15"),
            "2026-12-15"
        )

    def test_invalid_date(self):
        with self.assertRaises(ValueError):
            validate_date("15-12-2026")

    def test_future_date(self):
        future_date = (
            datetime.now().date() + timedelta(days=30)
        ).strftime("%Y-%m-%d")

        self.assertEqual(
            validate_future_date(future_date),
            future_date
        )

    def test_ticket_type(self):
        self.assertEqual(
            validate_ticket_type("VIP"),
            "vip"
        )

    def test_invalid_ticket_type(self):
        with self.assertRaises(ValueError):
            validate_ticket_type("Gold")


if __name__ == "__main__":
    unittest.main()
