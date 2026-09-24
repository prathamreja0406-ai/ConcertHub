
from datetime import datetime


from app.database import initialize_database
from app.utils import setup_logging
from app.auth import register_user, login_user
from app.concert_manager import ConcertManager
from app.booking_manager import BookingManager
from app.cancellation_manager import CancellationManager
from app.report_manager import ReportManager


# ==========================================================
# APPLICATION SERVICES
# ==========================================================

concert_manager = ConcertManager()
booking_manager = BookingManager()
cancellation_manager = CancellationManager()
report_manager = ReportManager()


# ==========================================================
# UI HELPERS
# ==========================================================

def print_header(title):

    print("\n" + "=" * 72)
    print(f"{title:^72}")
    print("=" * 72)


def pause():

    input("\nPress Enter to continue...")


def print_concerts(concerts):

    if not concerts:
        print("\nNo concerts found.")
        return

    print("\n" + "-" * 105)

    print(
        f"{'ID':<6}"
        f"{'Artist':<22}"
        f"{'City':<15}"
        f"{'Date':<14}"
        f"{'Genre':<15}"
        f"{'Seats':<12}"
    )

    print("-" * 105)

    for concert in concerts:

        print(
            f"{concert['concert_id']:<6}"
            f"{concert['artist'][:20]:<22}"
            f"{concert['city'][:13]:<15}"
            f"{concert['date']:<14}"
            f"{concert['genre'][:13]:<15}"
            f"{concert['available_seats']:<12}"
        )

    print("-" * 105)


# ==========================================================
# PUBLIC MENU
# ==========================================================

def browse_concerts():

    print_header("🎵 UPCOMING CONCERTS")

    concerts = concert_manager.get_all_concerts()

    print_concerts(concerts)

    pause()


def search_concerts():

    print_header("🔎 SEARCH CONCERTS")

    keyword = input(
        "Artist / venue / keyword "
        "(Enter to skip): "
    ).strip()

    city = input(
        "City (Enter to skip): "
    ).strip()

    genre = input(
        "Genre (Enter to skip): "
    ).strip()

    results = concert_manager.search_concerts(
        keyword=keyword or None,
        city=city or None,
        genre=genre or None
    )

    print_concerts(results)

    pause()


# ==========================================================
# REGISTRATION
# ==========================================================

def register():

    print_header("📝 CREATE ACCOUNT")

    try:

        name = input("Name     : ")
        email = input("Email    : ")
        password = input("Password : ")

        success, message = register_user(
            name,
            email,
            password
        )

        print(f"\n{'✓' if success else '✗'} {message}")

    except ValueError as error:

        print(f"\n✗ {error}")

    pause()


# ==========================================================
# USER MENU
# ==========================================================

def display_my_bookings(user):

    print_header("🎟️ MY BOOKINGS")

    bookings = booking_manager.get_user_bookings(
        user["user_id"]
    )

    if not bookings:

        print("You don't have any bookings yet.")

        pause()
        return

    for booking in bookings:

        print(f"""
Booking ID   : {booking['booking_id']}
Concert      : {booking['artist']}
Location     : {booking['venue']}, {booking['city']}
Date         : {booking['concert_date']}
Ticket Type  : {booking['ticket_type'].title()}
Quantity     : {booking['quantity']}
Amount       : ₹{booking['total_amount']:,.2f}
Status       : {booking['status']}
{"-" * 65}
""")

    pause()


def book_ticket(user):

    print_header("🎟️ BOOK TICKETS")

    try:

        concerts = concert_manager.get_all_concerts()

        print_concerts(concerts)

        concert_id = int(
            input("\nConcert ID : ")
        )

        ticket_type = input(
            "Ticket Type (Regular/VIP/Premium): "
        )

        quantity = int(
            input("Quantity : ")
        )

        success, message, booking_id = (
            booking_manager.create_booking(
                user["user_id"],
                concert_id,
                ticket_type,
                quantity
            )
        )

        if success:

            print("\n" + "=" * 60)
            print("             🎟️ BOOKING CONFIRMED")
            print("=" * 60)
            print(f"Booking ID : {booking_id}")
            print(message)
            print("=" * 60)

        else:

            print(f"\n✗ {message}")

    except ValueError as error:

        print(f"\n✗ Invalid input: {error}")

    pause()


def cancel_ticket(user):

    print_header("❌ CANCEL BOOKING")

    booking_id = input(
        "Booking ID : "
    ).strip().upper()

    booking = booking_manager.get_booking(
        booking_id
    )

    if not booking:

        print("\n✗ Booking not found.")
        pause()
        return

    if booking["user_id"] != user["user_id"]:

        print("\n✗ You can only cancel your own booking.")
        pause()
        return

    if booking["status"] != "CONFIRMED":

        print(
            f"\n✗ Booking is already "
            f"{booking['status'].lower()}."
        )

        pause()
        return

    refund = cancellation_manager.calculate_refund(
        booking["concert_date"],
        booking["total_amount"]
    )

    print(f"""
Concert             : {booking['artist']}
Tickets             : {booking['quantity']}
Original Amount     : ₹{booking['total_amount']:,.2f}
Days Remaining      : {refund['days_remaining']}
Refund Percentage   : {refund['refund_percentage']}%
Refund Amount       : ₹{refund['refund_amount']:,.2f}
Cancellation Charge : ₹{refund['cancellation_charge']:,.2f}
""")

    confirmation = input(
        "Confirm cancellation? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":

        print("\nCancellation aborted.")
        pause()
        return

    result = cancellation_manager.cancel_booking(
        user["user_id"],
        booking_id
    )

    if result["success"]:

        print("\n✓ Booking cancelled successfully.")
        print(
            f"✓ Refund Amount: "
            f"₹{result['refund_amount']:,.2f}"
        )

    else:

        print(f"\n✗ {result['message']}")

    pause()


# ==========================================================
# USER DASHBOARD
# ==========================================================

def user_menu(user):

    while True:

        print_header(
            f"🎵 CONCERTHUB — Welcome, {user['name']}"
        )

        print("""
1. Browse Concerts
2. Search Concerts
3. Book Tickets
4. My Bookings
5. Cancel Booking
6. Logout
""")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            browse_concerts()

        elif choice == "2":
            search_concerts()

        elif choice == "3":
            book_ticket(user)

        elif choice == "4":
            display_my_bookings(user)

        elif choice == "5":
            cancel_ticket(user)

        elif choice == "6":
            print("\n✓ Logged out successfully.")
            break

        else:
            print("\n✗ Invalid choice.")
            pause()


# ==========================================================
# ADMIN FUNCTIONS
# ==========================================================

def admin_view_concerts():

    print_header("🎼 CONCERT MANAGEMENT")

    concerts = concert_manager.get_all_concerts()

    print_concerts(concerts)

    pause()


def admin_add_concert():

    print_header("➕ ADD CONCERT")

    try:

        concert_id = int(
            input("Concert ID      : ")
        )

        artist = input(
            "Artist           : "
        )

        city = input(
            "City             : "
        )

        venue = input(
            "Venue            : "
        )

        date = input(
            "Date (YYYY-MM-DD): "
        )

        genre = input(
            "Genre            : "
        )

        regular_price = float(
            input("Regular Price    : ")
        )

        vip_price = float(
            input("VIP Price        : ")
        )

        premium_price = float(
            input("Premium Price    : ")
        )

        capacity = int(
            input("Capacity         : ")
        )

        success, message = (
            concert_manager.add_concert(
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
            )
        )

        print(
            f"\n{'✓' if success else '✗'} {message}"
        )

    except ValueError as error:

        print(f"\n✗ {error}")

    pause()


def admin_update_prices():

    print_header("💰 UPDATE CONCERT PRICES")

    try:

        concert_id = int(
            input("Concert ID : ")
        )

        regular = float(
            input("New Regular Price : ")
        )

        vip = float(
            input("New VIP Price : ")
        )

        premium = float(
            input("New Premium Price : ")
        )

        success, message = (
            concert_manager.update_prices(
                concert_id,
                regular,
                vip,
                premium
            )
        )

        print(
            f"\n{'✓' if success else '✗'} {message}"
        )

    except ValueError as error:

        print(f"\n✗ {error}")

    pause()


def admin_delete_concert():

    print_header("🗑️ DELETE CONCERT")

    try:

        concert_id = int(
            input("Concert ID : ")
        )

        confirmation = input(
            "Are you sure? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":

            print("\nDeletion cancelled.")
            pause()
            return

        success, message = (
            concert_manager.delete_concert(
                concert_id
            )
        )

        print(
            f"\n{'✓' if success else '✗'} {message}"
        )

    except ValueError as error:

        print(f"\n✗ {error}")

    pause()


def admin_view_bookings():

    print_header("🎟️ ALL BOOKINGS")

    bookings = booking_manager.get_all_bookings()

    if not bookings:

        print("No bookings found.")

    else:

        for booking in bookings:

            print(f"""
Booking ID : {booking['booking_id']}
Customer   : {booking['user_name']}
Email      : {booking['user_email']}
Concert    : {booking['artist']}
City       : {booking['city']}
Date       : {booking['concert_date']}
Tickets    : {booking['quantity']}
Type       : {booking['ticket_type'].title()}
Amount     : ₹{booking['total_amount']:,.2f}
Status     : {booking['status']}
{"-" * 70}
""")

    pause()


# ==========================================================
# ADMIN DASHBOARD
# ==========================================================

def admin_menu(user):

    while True:

        print_header(
            f"🛠️ ADMIN DASHBOARD — {user['name']}"
        )

        print("""
1. View Concerts
2. Add Concert
3. Update Concert Prices
4. Delete Concert
5. View All Bookings
6. View Sales Report
7. Logout
""")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":
            admin_view_concerts()

        elif choice == "2":
            admin_add_concert()

        elif choice == "3":
            admin_update_prices()

        elif choice == "4":
            admin_delete_concert()

        elif choice == "5":
            admin_view_bookings()

        elif choice == "6":
            report_manager.display_report()
            pause()

        elif choice == "7":
            print("\n✓ Admin logged out.")
            break

        else:
            print("\n✗ Invalid choice.")
            pause()


# ==========================================================
# LOGIN
# ==========================================================

def login():

    print_header("🔐 LOGIN")

    try:

        email = input("Email    : ")
        password = input("Password : ")

        user = login_user(
            email,
            password
        )

        if not user:

            print("\n✗ Invalid email or password.")
            pause()
            return

        print(
            f"\n✓ Welcome back, {user['name']}!"
        )

        if user["role"] == "admin":
            admin_menu(user)

        else:
            user_menu(user)

    except ValueError as error:

        print(f"\n✗ {error}")

        pause()


# ==========================================================
# MAIN MENU
# ==========================================================

def main_menu():

    while True:

        print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║                  🎵 CONCERTHUB 🎵                        ║
║                                                          ║
║       Concert Event & Ticket Management System           ║
║                                                          ║
╠══════════════════════════════════════════════════════════╣
║  1. Browse Concerts                                      ║
║  2. Search Concerts                                      ║
║  3. Create Account                                       ║
║  4. Login                                                ║
║  5. Exit                                                 ║
╚══════════════════════════════════════════════════════════╝
""")

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            browse_concerts()

        elif choice == "2":

            search_concerts()

        elif choice == "3":

            register()

        elif choice == "4":

            login()

        elif choice == "5":

            print(
                "\n🎵 Thank you for using ConcertHub!"
            )
            print(
                "Have a great concert experience! 🎶"
            )
            break

        else:

            print("\n✗ Invalid choice.")
            pause()


# ==========================================================
# APPLICATION ENTRY POINT
# ==========================================================

if __name__ == "__main__":
    logger = setup_logging()
    logger.info("ConcertHub application started.")

    initialize_database()

    print("\n✓ ConcertHub is ready.")

    main_menu()
