
from app.database import get_connection


class ReportManager:

    def get_summary(self):
        """
        Return overall booking and revenue statistics.
        """

        connection = get_connection()

        try:
            summary = connection.execute("""
                SELECT
                    COUNT(*) AS total_bookings,

                    COALESCE(
                        SUM(
                            CASE
                                WHEN status = 'CONFIRMED'
                                THEN quantity
                                ELSE 0
                            END
                        ),
                        0
                    ) AS tickets_sold,

                    COALESCE(
                        SUM(
                            CASE
                                WHEN status = 'CONFIRMED'
                                THEN total_amount
                                ELSE 0
                            END
                        ),
                        0
                    ) AS gross_revenue,

                    COALESCE(
                        SUM(
                            CASE
                                WHEN status = 'CANCELLED'
                                THEN 1
                                ELSE 0
                            END
                        ),
                        0
                    ) AS cancelled_bookings,

                    COALESCE(
                        SUM(
                            CASE
                                WHEN status = 'CANCELLED'
                                THEN refund_amount
                                ELSE 0
                            END
                        ),
                        0
                    ) AS total_refunds

                FROM bookings
            """).fetchone()

            gross_revenue = (
                summary["gross_revenue"] or 0
            )

            total_refunds = (
                summary["total_refunds"] or 0
            )

            net_revenue = (
                gross_revenue - total_refunds
            )

            return {
                "total_bookings": summary["total_bookings"],
                "tickets_sold": summary["tickets_sold"],
                "gross_revenue": gross_revenue,
                "cancelled_bookings": summary[
                    "cancelled_bookings"
                ],
                "total_refunds": total_refunds,
                "net_revenue": net_revenue
            }

        finally:
            connection.close()

    # --------------------------------------------------

    def get_ticket_type_breakdown(self):

        connection = get_connection()

        try:
            return connection.execute("""
                SELECT
                    ticket_type,

                    SUM(quantity) AS tickets_sold,

                    SUM(total_amount) AS revenue

                FROM bookings

                WHERE status = 'CONFIRMED'

                GROUP BY ticket_type

                ORDER BY revenue DESC
            """).fetchall()

        finally:
            connection.close()

    # --------------------------------------------------

    def get_concert_sales(self):

        connection = get_connection()

        try:
            return connection.execute("""
                SELECT
                    c.concert_id,
                    c.artist,
                    c.city,
                    c.date,

                    COALESCE(
                        SUM(
                            CASE
                                WHEN b.status = 'CONFIRMED'
                                THEN b.quantity
                                ELSE 0
                            END
                        ),
                        0
                    ) AS tickets_sold,

                    COALESCE(
                        SUM(
                            CASE
                                WHEN b.status = 'CONFIRMED'
                                THEN b.total_amount
                                ELSE 0
                            END
                        ),
                        0
                    ) AS revenue

                FROM concerts c

                LEFT JOIN bookings b
                    ON c.concert_id = b.concert_id

                GROUP BY c.concert_id

                ORDER BY tickets_sold DESC
            """).fetchall()

        finally:
            connection.close()

    # --------------------------------------------------

    def get_most_booked_concert(self):

        connection = get_connection()

        try:
            return connection.execute("""
                SELECT
                    c.concert_id,
                    c.artist,
                    c.city,
                    c.date,
                    SUM(b.quantity) AS tickets_sold

                FROM bookings b

                JOIN concerts c
                    ON b.concert_id = c.concert_id

                WHERE b.status = 'CONFIRMED'

                GROUP BY b.concert_id

                ORDER BY tickets_sold DESC

                LIMIT 1
            """).fetchone()

        finally:
            connection.close()

    # --------------------------------------------------

    def display_report(self):

        summary = self.get_summary()

        print("\n" + "=" * 72)
        print("                  📊 CONCERTHUB ANALYTICS")
        print("=" * 72)

        print(f"""
Total Bookings       : {summary['total_bookings']}
Confirmed Tickets    : {summary['tickets_sold']}
Cancelled Bookings   : {summary['cancelled_bookings']}

Gross Revenue        : ₹{summary['gross_revenue']:,.2f}
Total Refunds        : ₹{summary['total_refunds']:,.2f}
Net Revenue          : ₹{summary['net_revenue']:,.2f}
""")

        print("-" * 72)
        print("                 TICKET TYPE BREAKDOWN")
        print("-" * 72)

        breakdown = self.get_ticket_type_breakdown()

        if not breakdown:
            print("No confirmed ticket sales yet.")
        else:
            print(
                f"{'Type':<15}"
                f"{'Tickets':<12}"
                f"{'Revenue':<20}"
            )

            print("-" * 72)

            for item in breakdown:
                print(
                    f"{item['ticket_type'].title():<15}"
                    f"{item['tickets_sold']:<12}"
                    f"₹{item['revenue']:,.2f}"
                )

        print("\n" + "-" * 72)
        print("                    CONCERT SALES")
        print("-" * 72)

        concert_sales = self.get_concert_sales()

        if not concert_sales:
            print("No concerts available.")
        else:
            print(
                f"{'Artist':<22}"
                f"{'City':<15}"
                f"{'Tickets':<10}"
                f"{'Revenue':<15}"
            )

            print("-" * 72)

            for concert in concert_sales:
                print(
                    f"{concert['artist']:<22}"
                    f"{concert['city']:<15}"
                    f"{concert['tickets_sold']:<10}"
                    f"₹{concert['revenue']:,.2f}"
                )

        print("\n" + "-" * 72)
        print("                  MOST BOOKED CONCERT")
        print("-" * 72)

        popular = self.get_most_booked_concert()

        if popular:
            print(
                f"Artist       : {popular['artist']}"
            )
            print(
                f"City         : {popular['city']}"
            )
            print(
                f"Concert Date : {popular['date']}"
            )
            print(
                f"Tickets Sold : {popular['tickets_sold']}"
            )
        else:
            print("No confirmed bookings yet.")

        print("=" * 72)
