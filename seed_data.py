from app.database import initialize_database, get_connection
from app.concert_manager import ConcertManager


SAMPLE_CONCERTS = [
    (
        101,
        "Arijit Singh",
        "Indore",
        "Phoenix Citadel",
        "2026-10-12",
        "Bollywood",
        1499,
        2999,
        4999,
        5000
    ),
    (
        102,
        "AP Dhillon",
        "Delhi",
        "Jawaharlal Nehru Stadium",
        "2026-10-18",
        "Punjabi",
        1999,
        3999,
        5999,
        8000
    ),
    (
        103,
        "Shreya Ghoshal",
        "Mumbai",
        "Jio World Garden",
        "2026-10-25",
        "Classical",
        1799,
        3499,
        5499,
        6000
    ),
    (
        104,
        "The Local Train",
        "Bengaluru",
        "Palace Grounds",
        "2026-11-02",
        "Indie Rock",
        999,
        1999,
        3499,
        4500
    ),
    (
        105,
        "Anuv Jain",
        "Pune",
        "Mahalaxmi Lawns",
        "2026-12-15",
        "Indie",
        1299,
        2499,
        3999,
        3000
    )
]


def seed_concerts():
    initialize_database()

    manager = ConcertManager()

    added = 0
    skipped = 0

    for concert in SAMPLE_CONCERTS:
        success, message = manager.add_concert(*concert)

        if success:
            print(f"✓ {message}")
            added += 1
        else:
            print(f"• Skipped: {concert[1]} — {message}")
            skipped += 1

    print("\n" + "=" * 60)
    print("             DEMO DATA SETUP COMPLETE")
    print("=" * 60)
    print(f"Concerts added : {added}")
    print(f"Concerts skipped: {skipped}")
    print("=" * 60)


if __name__ == "__main__":
    seed_concerts()
