# ConcertHub — Project Statement

## 1. Problem Statement

Managing concert events and ticket bookings manually can lead to problems
such as incorrect seat availability, duplicate records, difficult booking
tracking, and inefficient cancellation handling.

ConcertHub is a command-line based Concert Event & Ticket Management System
designed to organize these operations through a structured Python application
with SQLite database storage.

The system provides separate workflows for normal users and administrators.
Users can discover concerts, create accounts, book tickets, view bookings,
and cancel bookings. Administrators can manage concerts, monitor bookings,
and view sales analytics.

---

## 2. Project Scope

ConcertHub focuses on the core workflow of a concert ticket management
system.

### Included

- User registration and login
- Secure password hashing
- Concert browsing
- Concert searching
- Ticket booking
- Multiple ticket categories
- Seat availability management
- Booking cancellation
- Project-defined refund calculation
- Administrator concert management
- Booking management
- Sales analytics
- SQLite database storage
- Input validation
- Transaction handling
- Application logging
- Automated unit testing

### Not Included

- Graphical user interface
- Online payment gateway
- Real payment processing
- Third-party ticketing APIs
- Real-time external event synchronization
- Mobile application

---

## 3. Target Users

### 3.1 Customers

Customers can:

- Create an account
- Login securely
- Browse concerts
- Search concerts
- Book tickets
- View their booking history
- Cancel confirmed bookings
- View refund information

### 3.2 Administrators

Administrators can:

- Add concerts
- View concerts
- Update ticket prices
- Delete eligible concerts
- View all bookings
- View sales and revenue reports

---

## 4. High-Level Features

1. User Authentication
2. Concert Management
3. Concert Search
4. Ticket Booking
5. Seat Inventory Management
6. Cancellation and Refund Management
7. Administrative Management
8. Sales Analytics
9. SQLite Database Storage
10. Input Validation and Error Handling
11. Logging
12. Automated Testing

---

## 5. Technology Stack

- Python 3.10+
- SQLite
- Python Standard Library
- unittest
- Git and GitHub

---

## 6. Application Type

ConcertHub is a command-line interface (CLI) application.

The application is intentionally GUI-free and can be executed from a terminal
using Python.

---

## 7. Refund Policy

ConcertHub uses the following refund policy as a project-defined business
rule:

- 7 or more days before the concert: 90% refund
- 3–6 days before the concert: 70% refund
- 1–2 days before the concert: 40% refund
- Same day or after the concert: 0% refund

This policy is part of the academic project design and does not represent
the policy of any real-world ticketing platform.
