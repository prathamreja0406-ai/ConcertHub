

# 🎵 ConcertHub

## Concert Event & Ticket Management System

ConcertHub is a Python-based command-line application for managing concert
events, ticket bookings, cancellations, users, and administrative reports.

The project demonstrates core Python programming concepts together with
modular architecture, object-oriented programming, SQLite database
management, validation, secure password hashing, transaction handling,
logging, and automated testing.

---

## ✨ Features

### 👤 User Features

- User registration
- Secure login
- Browse concerts
- Search concerts
- Book tickets
- Regular, VIP, and Premium ticket categories
- View personal bookings
- Cancel confirmed bookings
- Automatic refund calculation

### 🔐 Admin Features

- Add concerts
- View concerts
- Update ticket prices
- Delete concerts when eligible
- View all bookings
- View sales analytics
- Revenue and refund summary
- Ticket-type breakdown
- Most-booked concert analysis

### ⚙️ Technical Features

- SQLite persistent storage

- Random password salts
- Input validation
- SQLite transactions
- Foreign key constraints
- Error handling
- Application logging
- Automated unit tests
- Modular Python package structure

---

## 🏗️ Project Architecture

```text


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
