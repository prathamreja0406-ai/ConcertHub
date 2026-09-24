from datetime import datetime, timedelta

from tests.test_helpers import ConcertHubTestCase

from app.auth import register_user, login_user
from app.concert_manager import ConcertManager
from app.booking_manager import BookingManager


class TestBookingManager(ConcertHubTestCase):

    def setUp(self):
        super().setUp()

        self.concert_manager = ConcertManager()
        self.booking_manager = BookingManager()

        register_user(
            "Booking User",
            "booking@example.com",
            "Password@123"
        )

        self.user = login_user(
            "booking@example.com",
            "Password@123"
        )

        future_date = (
            datetime.now().date() + timedelta(days=60)
        ).strftime("%Y-%m-%d")

        self.concert_manager.add_concert(
            601,
            "Booking Artist",
            "Bhopal",
            "Booking Arena",
            future_date,
            "Rock",
            1000,
            2000,
            3000,
            100
        )

    def test_create_booking(self):
        success, message, booking_id = (
            self.booking_manager.create_booking(
                self.user["user_id"],
                601,
                "VIP",
                3
            )
        )

        self.assertTrue(success)
        self.assertIsNotNone(booking_id)
        self.assertIn("Booking confirmed", message)

        concert = self.concert_manager.get_concert(601)

        self.assertEqual(concert["available_seats"], 97)

    def test_overbooking_rejected(self):
        success, message, booking_id = (
            self.booking_manager.create_booking(
                self.user["user_id"],
                601,
                "Premium",
                101
            )
        )

        self.assertFalse(success)
        self.assertIsNone(booking_id)
        self.assertIn("available", message.lower())

    def test_user_bookings(self):
        self.booking_manager.create_booking(
            self.user["user_id"],
            601,
            "Regular",
            2
        )

        bookings = self.booking_manager.get_user_bookings(
            self.user["user_id"]
        )

        self.assertEqual(len(bookings), 1)
        self.assertEqual(bookings[0]["quantity"], 2)
        self.assertEqual(bookings[0]["ticket_type"], "regular")


if __name__ == "__main__":
    import unittest
    unittest.main()
