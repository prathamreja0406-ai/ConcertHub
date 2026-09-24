from datetime import datetime, timedelta

from tests.test_helpers import ConcertHubTestCase

from app.concert_manager import ConcertManager


class TestConcertManager(ConcertHubTestCase):

    def setUp(self):
        super().setUp()
        self.manager = ConcertManager()

        self.future_date = (
            datetime.now().date() + timedelta(days=60)
        ).strftime("%Y-%m-%d")

    def test_add_concert(self):
        success, message = self.manager.add_concert(
            501,
            "Test Artist",
            "Indore",
            "Test Arena",
            self.future_date,
            "Indie",
            999,
            1999,
            2999,
            1000
        )

        self.assertTrue(success)

        concert = self.manager.get_concert(501)

        self.assertIsNotNone(concert)
        self.assertEqual(concert["artist"], "Test Artist")
        self.assertEqual(concert["capacity"], 1000)
        self.assertEqual(concert["available_seats"], 1000)

    def test_search_concert(self):
        self.manager.add_concert(
            502,
            "Search Artist",
            "Delhi",
            "Search Arena",
            self.future_date,
            "Rock",
            1000,
            2000,
            3000,
            500
        )

        results = self.manager.search_concerts(
            keyword="Search Artist"
        )

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["artist"], "Search Artist")

    def test_invalid_price_order(self):
        with self.assertRaises(ValueError):
            self.manager.add_concert(
                503,
                "Invalid Artist",
                "Mumbai",
                "Arena",
                self.future_date,
                "Pop",
                3000,
                2000,
                1000,
                500
            )

    def test_past_date_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.add_concert(
                504,
                "Past Artist",
                "Pune",
                "Arena",
                "2020-01-01",
                "Pop",
                1000,
                2000,
                3000,
                500
            )


if __name__ == "__main__":
    import unittest
    unittest.main()
