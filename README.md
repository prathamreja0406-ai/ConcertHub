


ConcertHub
A command-line concert management and ticket booking system built in Python.
ConcertHub simulates a full-fledged ticketing platform right from the terminal. It handles everything from user registration and ticket reservations to admin management, revenue analytics, and transaction security, backed by an SQLite database.
Features
For Users
Account Management: Register and log in securely.
Concert Discovery: Browse all upcoming events or search for specific artists/venues.
Ticket Booking: Reserve tickets across Regular, VIP, and Premium tiers.
Booking History & Refunds: View active bookings and cancel tickets (with automatic refund calculation).
For Admins
Event Management: Add new concerts, update pricing on the fly, or clean up past events.
Sales Analytics: Track total revenue, refund summaries, ticket tier performance, and top-selling concerts.
Overview: View all system-wide bookings in real time.
Tech Stack & Architecture Highlights
Database: SQLite for local storage, complete with foreign keys and atomic transaction handling.
Security: Password hashing using PBKDF2-HMAC-SHA256 with random per-user salts.
Code Quality: Built using OOP principles, custom input validation, logging, and automated unit tests.


ConcertHub
│
├── main.py
├── setup_admin.py
│
├── app/
│   ├── database.py
│   ├── models.py
│   ├── auth.py
│   ├── concert_manager.py
│   ├── booking_manager.py
│   ├── cancellation_manager.py
│   ├── report_manager.py
│   ├── validators.py
│   └── utils.py
│
├── tests/
│   ├── test_validators.py
│   ├── test_auth.py
│   ├── test_concerts.py
│   ├── test_bookings.py
│   └── test_cancellation.py
│
├── data/
│   └── concert_hub.db
│
└── docs/
    └── diagrams/
