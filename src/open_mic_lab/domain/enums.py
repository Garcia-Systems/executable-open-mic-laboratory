"""Shared domain enumerations."""

from enum import StrEnum


class Genre(StrEnum):
    """Practical genre categories for repertoire exploration."""

    FOLK = "folk"
    BLUES = "blues"
    JAZZ = "jazz"
    POP = "pop"
    ORIGINAL = "original"
    TRADITIONAL = "traditional"


class Mood(StrEnum):
    """Broad performance moods."""

    REFLECTIVE = "reflective"
    WARM = "warm"
    PLAYFUL = "playful"
    MELANCHOLY = "melancholy"
    ENERGETIC = "energetic"
    RESOLUTE = "resolute"


class Instrument(StrEnum):
    """Primary performance instruments."""

    PIANO_VOCAL = "piano/vocal"
    GUITAR_VOCAL = "guitar/vocal"
    A_CAPPELLA = "a cappella"
    UKULELE_VOCAL = "ukulele/vocal"


class Difficulty(StrEnum):
    """Arrangement difficulty levels."""

    SIMPLE = "simple"
    MODERATE = "moderate"
    CHALLENGING = "challenging"


class PerformanceStatus(StrEnum):
    """Current readiness workflow status."""

    IDEA = "idea"
    LEARNING = "learning"
    DEVELOPING = "developing"
    NEARLY_READY = "nearly ready"
    PERFORMANCE_READY = "performance ready"


class VenueType(StrEnum):
    """Venue categories for early experiments."""

    OPEN_MIC = "open mic"
    HOUSE_CONCERT = "house concert"
    CAFE = "cafe"
    COMMUNITY_EVENT = "community event"
