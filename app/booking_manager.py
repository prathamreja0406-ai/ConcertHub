
import uuid
from datetime import datetime

from app.database import get_connection
from app.validators import (
    validate_positive_integer,
    validate_ticket_type
)


class BookingManager:

    def create_booking(
        self,
        user_id,
        concert_id,
        ticket_type,
        quantity
    ):
        """
        Create a confirmed ticket booking.

        Returns:
            (success, message, booking_id)
        """

        quantity = validate_positive_integer(
            quantity,
            "Ticket quantity"
        )

        ticket_type = validate_ticket_type(
            ticket_type
        )

        connection = get_connection()

        try:
            # Start an immediate transaction so the seat check
            # and seat update happen safely together.
            connection.execute("BEGIN IMMEDIATE")

            concert = connection.execute("""
                SELECT *
                FROM concerts
                WHERE concert_id = ?
            """, (concert_id,)).fetchone()

            if not concert:
                connection.rollback()
                return False, "Concert not found.", None

            prices = {
                "regular": concert["regular_price"],
                "vip": concert["vip_price"],
                "premium": concert["premium_price"]
            }

            price_per_ticket = prices[ticket_type]

            if quantity > concert["available_seats"]:
                connection.rollback()

                return (
                    False,
                    (
                        f"Only {concert['available_seats']} "
                        f"seats are available."
                    ),
                    None
                )

            total_amount = (
                price_per_ticket * quantity
            )

            booking_id = (
                "BK-"
                + uuid.uuid4().hex[:8].upper()
            )

            booking_time = datetime.now().isoformat(
                timespec="seconds"
            )

            connection.execute("""
                INSERT INTO bookings (
                    booking_id,
                    user_id,
                    concert_id,
                    ticket_type,
                    quantity,
                    price_per_ticket,
                    total_amount,
                    booking_time,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                booking_id,
                user_id,
                concert_id,
                ticket_type,
                quantity,
                price_per_ticket,
                total_amount,
                booking_time,
                "CONFIRMED"
            ))

            connection.execute("""
                UPDATE concerts
                SET available_seats =
                    available_seats - ?
                WHERE concert_id = ?
            """, (
                quantity,
                concert_id
            ))

            connection.commit()

            return (
                True,
                (
                    f"Booking confirmed successfully. "
                    f"Total amount: ₹{total_amount:,.2f}"
                ),
                booking_id
            )

        except Exception as error:

            connection.rollback()

            return (
                False,
                f"Booking failed: {error}",
                None
            )

        finally:
            connection.close()

    # --------------------------------------------------

    def get_booking(self, booking_id):

        connection = get_connection()

        try:
            return connection.execute("""
                SELECT
                    b.*,
                    u.name AS user_name,
                    u.email AS user_email,
                    c.artist,
                    c.city,
                    c.venue,
                    c.date AS concert_date
                FROM bookings b

                JOIN users u
                    ON b.user_id = u.user_id

                JOIN concerts c
                    ON b.concert_id = c.concert_id

                WHERE b.booking_id = ?
            """, (booking_id,)).fetchone()

        finally:
            connection.close()

    # --------------------------------------------------

    def get_user_bookings(self, user_id):

        connection = get_connection()

        try:
            return connection.execute("""
                SELECT
                    b.booking_id,
                    b.ticket_type,
                    b.quantity,
                    b.price_per_ticket,
                    b.total_amount,
                    b.booking_time,
                    b.status,

                    c.artist,
                    c.city,
                    c.venue,
                    c.date AS concert_date

                FROM bookings b

                JOIN concerts c
                    ON b.concert_id = c.concert_id

                WHERE b.user_id = ?

                ORDER BY b.booking_time DESC
            """, (user_id,)).fetchall()

        finally:
            connection.close()

    # --------------------------------------------------

    def get_all_bookings(self):

        connection = get_connection()

        try:
            return connection.execute("""
                SELECT
                    b.booking_id,
                    b.ticket_type,
                    b.quantity,
                    b.total_amount,
                    b.booking_time,
                    b.status,

                    u.name AS user_name,
                    u.email AS user_email,

                    c.artist,
                    c.city,
                    c.date AS concert_date

                FROM bookings b

                JOIN users u
                    ON b.user_id = u.user_id

                JOIN concerts c
                    ON b.concert_id = c.concert_id

                ORDER BY b.booking_time DESC
            """).fetchall()

        finally:
            connection.close()
