from tests.test_helpers import ConcertHubTestCase

from app.auth import register_user, login_user


class TestAuthentication(ConcertHubTestCase):

    def test_register_user(self):
        success, message = register_user(
            "Test User",
            "test@example.com",
            "Password@123"
        )

        self.assertTrue(success)
        self.assertIn("successfully", message.lower())

    def test_duplicate_email(self):
        register_user(
            "Test User",
            "duplicate@example.com",
            "Password@123"
        )

        success, message = register_user(
            "Another User",
            "duplicate@example.com",
            "Password@123"
        )

        self.assertFalse(success)
        self.assertIn("already exists", message.lower())

    def test_successful_login(self):
        register_user(
            "Login User",
            "login@example.com",
            "Password@123"
        )

        user = login_user(
            "login@example.com",
            "Password@123"
        )

        self.assertIsNotNone(user)
        self.assertEqual(user["email"], "login@example.com")
        self.assertEqual(user["role"], "user")

    def test_wrong_password(self):
        register_user(
            "Login User",
            "wrong@example.com",
            "Password@123"
        )

        user = login_user(
            "wrong@example.com",
            "WrongPassword"
        )

        self.assertIsNone(user)


if __name__ == "__main__":
    import unittest
    unittest.main()
