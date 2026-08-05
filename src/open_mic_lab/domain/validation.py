"""Validation helpers for learner-friendly domain errors."""

from decimal import Decimal

RATING_MIN = Decimal("0")
RATING_MAX = Decimal("10")


def require_text(value: str, field_name: str) -> None:
    """Require a non-blank text value."""
    if not value.strip():
        raise ValueError(f"{field_name} cannot be blank.")


def require_positive_int(value: int, field_name: str) -> None:
    """Require a positive integer."""
    if value <= 0:
        raise ValueError(f"{field_name} must be positive.")


def require_non_negative_int(value: int, field_name: str) -> None:
    """Require a non-negative integer."""
    if value < 0:
        raise ValueError(f"{field_name} cannot be negative.")


def require_rating(value: Decimal, field_name: str) -> None:
    """Require a 0-10 learner rating."""
    if value < RATING_MIN or value > RATING_MAX:
        raise ValueError(f"{field_name} must be between 0 and 10.")


def require_int_between(value: int, field_name: str, minimum: int, maximum: int) -> None:
    """Require an integer within an inclusive range."""
    if value < minimum or value > maximum:
        raise ValueError(f"{field_name} must be between {minimum} and {maximum}.")
