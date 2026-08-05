"""Venue model."""

from dataclasses import dataclass
from decimal import Decimal

from open_mic_lab.domain.enums import VenueType
from open_mic_lab.domain.validation import (
    require_non_negative_int,
    require_positive_int,
    require_rating,
    require_text,
)


@dataclass(frozen=True, slots=True)
class Venue:
    """A performance context with constraints and affordances."""

    identifier: str
    name: str
    venue_type: VenueType
    expected_audience_size: int
    audience_familiarity_preference: Decimal
    available_piano: bool
    amplification_available: bool
    typical_set_duration_minutes: int
    notes: str = ""

    def __post_init__(self) -> None:
        require_text(self.identifier, "Venue identifier")
        require_text(self.name, "Venue name")
        require_non_negative_int(self.expected_audience_size, "Expected audience size")
        require_rating(self.audience_familiarity_preference, "Audience familiarity preference")
        require_positive_int(self.typical_set_duration_minutes, "Typical set duration")
