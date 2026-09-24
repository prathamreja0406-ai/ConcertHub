from datetime import datetime, timedelta

from tests.test_helpers import ConcertHubTestCase

from app.auth import register_user, login_user
from app.concert_manager import ConcertManager
from app.booking_manager import BookingManager
from app.cancellation_manager import CancellationManager


class TestCancellationManager(ConcertHubTestCase):

    def setUp(self):
        super().setUp()

        self.concert_manager = ConcertManager()
        self.booking_manager = BookingManager()
        self.cancellation_manager = CancellationManager()

        register_user(
            "Cancel User",
            "cancel@example.com",
            "Password@123"
        )

        self.user = login_user(
            "cancel@example.com",
            "Password@123"
        )

        self.future_date = (
            datetime.now().date() + timedelta(days=30)
        ).strftime("%Y-%m-%d")

        self.concert_manager.add_concert(
            701,
            "Cancel Artist",
            "Indore",
            "Cancel Arena",
            self.future_date,
            "Pop",
            1000,
            2000,
            3000,
            100
        )

    def test_refund_calculation(self):
        refund = self.cancellation_manager.calculate_refund(
            self.future_date,
            3000
        )

        self.assertEqual(refund["refund_percentage"], 90)
        self.assertEqual(refund["refund_amount"], 2700)

    def test_cancel_booking(self):
        success, message, booking_id = (
            self.booking_manager.create_booking(
                self.user["user_id"],
                701,
                "Premium",
                2
            )
        )

        self.assertTrue(success)

        result = self.cancellation_manager.cancel_booking(
            self.user["user_id"],
            booking_id
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["refund_percentage"], 90)
        self.assertEqual(result["refund_amount"], 5400)

        booking = self.booking_manager.get_booking(booking_id)

        self.assertEqual(booking["status"], "CANCELLED")
        self.assertEqual(booking["refund_amount"], 5400)

        concert = self.concert_manager.get_concert(701)

        self.assertEqual(concert["available_seats"], 100)


if __name__ == "__main__":
    import unittest
    unittest.main()
