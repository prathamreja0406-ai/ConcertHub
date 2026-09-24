
from datetime import datetime

from app.database import get_connection


class CancellationManager:

    def calculate_refund(self, concert_date, total_amount):
        """
        Calculate refund according to ConcertHub's
        project-defined cancellation policy.

        Policy:
        7+ days   -> 90% refund
        3-6 days  -> 70% refund
        1-2 days  -> 40% refund
        Same day  -> 0% refund
        """

        concert_date = datetime.strptime(
            concert_date,
            "%Y-%m-%d"
        ).date()

        today = datetime.now().date()

        days_remaining = (
            concert_date - today
        ).days

        if days_remaining >= 7:
            refund_percentage = 90

        elif days_remaining >= 3:
            refund_percentage = 70

        elif days_remaining >= 1:
            refund_percentage = 40

        else:
            refund_percentage = 0

        refund_amount = (
            total_amount * refund_percentage / 100
        )

        cancellation_charge = (
            total_amount - refund_amount
        )

        return {
            "days_remaining": days_remaining,
            "refund_percentage": refund_percentage,
            "refund_amount": refund_amount,
            "cancellation_charge": cancellation_charge
        }

    # --------------------------------------------------

    def cancel_booking(
        self,
        user_id,
        booking_id
    ):
        """
        Cancel a user's confirmed booking and
        restore the reserved seats.
        """

        connection = get_connection()

        try:

            connection.execute("BEGIN IMMEDIATE")

            booking = connection.execute("""
                SELECT
                    b.*,
                    c.artist,
                    c.date AS concert_date,
                    c.capacity,
                    c.available_seats
                FROM bookings b

                JOIN concerts c
                    ON b.concert_id = c.concert_id

                WHERE b.booking_id = ?
                  AND b.user_id = ?
            """, (
                booking_id,
                user_id
            )).fetchone()

            if not booking:
                connection.rollback()

                return {
                    "success": False,
                    "message": "Booking not found."
                }

            if booking["status"] != "CONFIRMED":
                connection.rollback()

                return {
                    "success": False,
                    "message": (
                        "Only confirmed bookings "
                        "can be cancelled."
                    )
                }

            refund = self.calculate_refund(
                booking["concert_date"],
                booking["total_amount"]
            )

            # Restore tickets to concert inventory.
            new_available_seats = (
                booking["available_seats"]
                + booking["quantity"]
            )

            if new_available_seats > booking["capacity"]:
                connection.rollback()

                return {
                    "success": False,
                    "message": (
                        "Seat inventory validation failed."
                    )
                }

            connection.execute("""
                UPDATE concerts
                SET available_seats = ?
                WHERE concert_id = ?
            """, (
                new_available_seats,
                booking["concert_id"]
            ))

            # Mark booking as cancelled and save refund.
            connection.execute("""
                UPDATE bookings
                SET
                    status = 'CANCELLED',
                    refund_amount = ?,
                    cancellation_time = ?
                WHERE booking_id = ?
            """, (
                refund["refund_amount"],
                datetime.now().isoformat(
                    timespec="seconds"
                ),
                booking_id
            ))

            connection.commit()

            return {
                "success": True,
                "message": "Booking cancelled successfully.",
                "booking_id": booking_id,
                "artist": booking["artist"],
                "quantity": booking["quantity"],
                "original_amount": booking["total_amount"],
                "refund_percentage": (
                    refund["refund_percentage"]
                ),
                "refund_amount": (
                    refund["refund_amount"]
                ),
                "cancellation_charge": (
                    refund["cancellation_charge"]
                ),
                "days_remaining": (
                    refund["days_remaining"]
                )
            }

        except Exception as error:

            connection.rollback()

            return {
                "success": False,
                "message": (
                    f"Cancellation failed: {error}"
                )
            }

        finally:
            connection.close()
