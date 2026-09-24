
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    user_id: int
    name: str
    email: str
    role: str = "user"

    def is_admin(self) -> bool:
        return self.role.lower() == "admin"


@dataclass
class Concert:
    concert_id: int
    artist: str
    city: str
    venue: str
    date: str
    genre: str
    regular_price: float
    vip_price: float
    premium_price: float
    capacity: int
    available_seats: int

    def get_ticket_price(self, ticket_type: str) -> Optional[float]:
        prices = {
            "regular": self.regular_price,
            "vip": self.vip_price,
            "premium": self.premium_price
        }

        return prices.get(ticket_type.lower())

    def booked_seats(self) -> int:
        return self.capacity - self.available_seats

    def occupancy_percentage(self) -> float:
        if self.capacity == 0:
            return 0.0

        return (
            self.booked_seats() / self.capacity
        ) * 100

    def has_availability(self, quantity: int) -> bool:
        return (
            quantity > 0
            and quantity <= self.available_seats
        )


@dataclass
class Booking:
    booking_id: str
    user_id: int
    concert_id: int
    ticket_type: str
    quantity: int
    price_per_ticket: float
    total_amount: float
    booking_time: str
    status: str = "CONFIRMED"
    refund_amount: float = 0.0
