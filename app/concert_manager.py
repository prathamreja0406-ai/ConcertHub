
from app.database import get_connection
from app.validators import (
    validate_name,
    validate_positive_integer,
    validate_non_negative_number,
    validate_future_date
)


class ConcertManager:

    def add_concert(
        self,
        concert_id,
        artist,
        city,
        venue,
        date,
        genre,
        regular_price,
        vip_price,
        premium_price,
        capacity
    ):
        concert_id = validate_positive_integer(
            concert_id, "Concert ID"
        )

        capacity = validate_positive_integer(
            capacity, "Capacity"
        )

        regular_price = validate_non_negative_number(
            regular_price, "Regular price"
        )

        vip_price = validate_non_negative_number(
            vip_price, "VIP price"
        )

        premium_price = validate_non_negative_number(
            premium_price, "Premium price"
        )

        artist = validate_name(artist)
        city = validate_name(city)
        venue = validate_name(venue)
        genre = validate_name(genre)
        date = validate_future_date(date)

        if not (
            regular_price <= vip_price <= premium_price
        ):
            raise ValueError(
                "Ticket prices must follow: "
                "Regular <= VIP <= Premium."
            )

        connection = get_connection()

        try:
            connection.execute("""
                INSERT INTO concerts (
                    concert_id,
                    artist,
                    city,
                    venue,
                    date,
                    genre,
                    regular_price,
                    vip_price,
                    premium_price,
                    capacity,
                    available_seats
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                concert_id,
                artist,
                city,
                venue,
                date,
                genre,
                regular_price,
                vip_price,
                premium_price,
                capacity,
                capacity
            ))

            connection.commit()

            return True, (
                f"Concert '{artist}' added successfully."
            )

        except Exception as error:
            connection.rollback()

            if "UNIQUE constraint failed" in str(error):
                return False, "Concert ID already exists."

            return False, "Unable to add concert."

        finally:
            connection.close()

    # --------------------------------------------------

    def get_all_concerts(self):

        connection = get_connection()

        try:
            return connection.execute("""
                SELECT *
                FROM concerts
                ORDER BY date ASC
            """).fetchall()

        finally:
            connection.close()

    # --------------------------------------------------

    def get_concert(self, concert_id):

        connection = get_connection()

        try:
            return connection.execute("""
                SELECT *
                FROM concerts
                WHERE concert_id = ?
            """, (concert_id,)).fetchone()

        finally:
            connection.close()

    # --------------------------------------------------

    def search_concerts(
        self,
        keyword=None,
        city=None,
        genre=None
    ):

        connection = get_connection()

        query = """
            SELECT *
            FROM concerts
            WHERE 1 = 1
        """

        parameters = []

        if keyword:
            keyword = f"%{keyword.strip()}%"

            query += """
                AND (
                    artist LIKE ?
                    OR venue LIKE ?
                    OR city LIKE ?
                    OR genre LIKE ?
                )
            """

            parameters.extend([
                keyword,
                keyword,
                keyword,
                keyword
            ])

        if city:
            query += " AND city LIKE ?"
            parameters.append(f"%{city.strip()}%")

        if genre:
            query += " AND genre LIKE ?"
            parameters.append(f"%{genre.strip()}%")

        query += " ORDER BY date ASC"

        try:
            return connection.execute(
                query,
                parameters
            ).fetchall()

        finally:
            connection.close()

    # --------------------------------------------------

    def update_prices(
        self,
        concert_id,
        regular_price,
        vip_price,
        premium_price
    ):

        regular_price = validate_non_negative_number(
            regular_price, "Regular price"
        )

        vip_price = validate_non_negative_number(
            vip_price, "VIP price"
        )

        premium_price = validate_non_negative_number(
            premium_price, "Premium price"
        )

        if not (
            regular_price <= vip_price <= premium_price
        ):
            raise ValueError(
                "Ticket prices must follow: "
                "Regular <= VIP <= Premium."
            )

        connection = get_connection()

        try:

            cursor = connection.execute("""
                UPDATE concerts
                SET
                    regular_price = ?,
                    vip_price = ?,
                    premium_price = ?
                WHERE concert_id = ?
            """, (
                regular_price,
                vip_price,
                premium_price,
                concert_id
            ))

            if cursor.rowcount == 0:
                return False, "Concert not found."

            connection.commit()

            return True, "Concert prices updated successfully."

        except Exception:
            connection.rollback()
            return False, "Unable to update concert."

        finally:
            connection.close()

    # --------------------------------------------------

    def delete_concert(self, concert_id):

        connection = get_connection()

        try:

            concert = connection.execute("""
                SELECT concert_id
                FROM concerts
                WHERE concert_id = ?
            """, (concert_id,)).fetchone()

            if not concert:
                return False, "Concert not found."

            confirmed_bookings = connection.execute("""
                SELECT COUNT(*) AS total
                FROM bookings
                WHERE concert_id = ?
                AND status = 'CONFIRMED'
            """, (concert_id,)).fetchone()

            if confirmed_bookings["total"] > 0:
                return False, (
                    "Concert cannot be deleted because "
                    "confirmed bookings exist."
                )

            connection.execute("""
                DELETE FROM concerts
                WHERE concert_id = ?
            """, (concert_id,))

            connection.commit()

            return True, "Concert deleted successfully."

        except Exception:
            connection.rollback()
            return False, "Unable to delete concert."

        finally:
            connection.close()
