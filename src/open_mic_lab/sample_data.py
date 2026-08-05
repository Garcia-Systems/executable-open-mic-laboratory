"""Deterministic sample repertoire for examples, tests, and CLI demos."""

from datetime import date
from decimal import Decimal

from open_mic_lab.domain import (
    Difficulty,
    Genre,
    Instrument,
    Mood,
    PerformanceStatus,
    PerformanceVersion,
    PracticeSession,
    Repertoire,
    SetList,
    Song,
    Venue,
    VenueType,
)


def build_sample_repertoire() -> Repertoire:
    """Build six songs and seven performance versions with deterministic ordering."""
    rep = Repertoire()
    songs = (
        Song(
            "river-road",
            "River Road at Dusk",
            "Mara Vale",
            Genre.FOLK,
            "G",
            92,
            "4/4",
            Mood.REFLECTIVE,
            Decimal("3"),
            Decimal("8"),
            Decimal("2"),
        ),
        Song(
            "lantern-swing",
            "Lantern Swing",
            "Public Domain Style",
            Genre.JAZZ,
            "F",
            132,
            "4/4",
            Mood.PLAYFUL,
            Decimal("5"),
            Decimal("4"),
            Decimal("6"),
        ),
        Song(
            "harbor-bell",
            "Harbor Bell",
            "Traditional",
            Genre.TRADITIONAL,
            "D",
            104,
            "3/4",
            Mood.WARM,
            Decimal("8"),
            Decimal("6"),
            Decimal("7"),
        ),
        Song(
            "blue-ticket",
            "Blue Ticket Blues",
            "Jonas Reed",
            Genre.BLUES,
            "E",
            88,
            "4/4",
            Mood.MELANCHOLY,
            Decimal("4"),
            Decimal("5"),
            Decimal("5"),
        ),
        Song(
            "window-original",
            "Window Light",
            "Learner Original",
            Genre.ORIGINAL,
            "A",
            76,
            "4/4",
            Mood.RESOLUTE,
            Decimal("1"),
            Decimal("9"),
            Decimal("3"),
        ),
        Song(
            "last-train-home",
            "Last Train Home",
            "Fictional Standard",
            Genre.POP,
            "C",
            148,
            "4/4",
            Mood.ENERGETIC,
            Decimal("7"),
            Decimal("5"),
            Decimal("9"),
        ),
    )
    for song in songs:
        rep.add_song(song)
    versions = (
        PerformanceVersion(
            "river-guitar-original",
            "river-road",
            "G",
            92,
            Instrument.GUITAR_VOCAL,
            Difficulty.MODERATE,
            Decimal("6"),
            Decimal("7"),
            Decimal("7"),
            Decimal("5"),
            PerformanceStatus.DEVELOPING,
            20,
            "Original key and tempo.",
        ),
        PerformanceVersion(
            "river-guitar-lowered",
            "river-road",
            "E",
            84,
            Instrument.GUITAR_VOCAL,
            Difficulty.SIMPLE,
            Decimal("8"),
            Decimal("8"),
            Decimal("8"),
            Decimal("7"),
            PerformanceStatus.NEARLY_READY,
            15,
            "Lowered key for vocal comfort.",
        ),
        PerformanceVersion(
            "lantern-piano",
            "lantern-swing",
            "F",
            126,
            Instrument.PIANO_VOCAL,
            Difficulty.CHALLENGING,
            Decimal("6"),
            Decimal("6"),
            Decimal("5"),
            Decimal("5"),
            PerformanceStatus.LEARNING,
            25,
        ),
        PerformanceVersion(
            "harbor-guitar",
            "harbor-bell",
            "D",
            104,
            Instrument.GUITAR_VOCAL,
            Difficulty.SIMPLE,
            Decimal("9"),
            Decimal("9"),
            Decimal("8"),
            Decimal("8"),
            PerformanceStatus.PERFORMANCE_READY,
            10,
        ),
        PerformanceVersion(
            "blue-ticket-guitar",
            "blue-ticket",
            "E",
            88,
            Instrument.GUITAR_VOCAL,
            Difficulty.MODERATE,
            Decimal("7"),
            Decimal("6"),
            Decimal("6"),
            Decimal("7"),
            PerformanceStatus.DEVELOPING,
            15,
        ),
        PerformanceVersion(
            "window-piano",
            "window-original",
            "A",
            72,
            Instrument.PIANO_VOCAL,
            Difficulty.MODERATE,
            Decimal("8"),
            Decimal("7"),
            Decimal("7"),
            Decimal("8"),
            PerformanceStatus.NEARLY_READY,
            30,
        ),
        PerformanceVersion(
            "train-guitar-closer",
            "last-train-home",
            "C",
            148,
            Instrument.GUITAR_VOCAL,
            Difficulty.SIMPLE,
            Decimal("9"),
            Decimal("8"),
            Decimal("9"),
            Decimal("8"),
            PerformanceStatus.PERFORMANCE_READY,
            12,
        ),
    )
    for version in versions:
        rep.add_performance_version(version)
    return rep


def sample_practice_sessions() -> tuple[PracticeSession, ...]:
    """Return deterministic practice evidence."""
    return (
        PracticeSession(
            "practice-river-1",
            "river-guitar-lowered",
            date(2026, 7, 20),
            35,
            82,
            4,
            Decimal("8"),
            Decimal("8"),
            Decimal("8"),
            Decimal("7"),
        ),
        PracticeSession(
            "practice-river-2",
            "river-guitar-lowered",
            date(2026, 7, 25),
            30,
            84,
            3,
            Decimal("8"),
            Decimal("8"),
            Decimal("8"),
            Decimal("7"),
        ),
        PracticeSession(
            "practice-train-1",
            "train-guitar-closer",
            date(2026, 7, 26),
            45,
            148,
            2,
            Decimal("9"),
            Decimal("9"),
            Decimal("8"),
            Decimal("8"),
        ),
    )


def sample_venue() -> Venue:
    """Return a sample open-mic venue."""
    return Venue(
        "corner-cafe", "Corner Cafe Open Mic", VenueType.OPEN_MIC, 45, Decimal("6"), True, True, 15
    )


def sample_setlist() -> SetList:
    """Return a sample 15-minute set."""
    return SetList(
        "sample-15",
        "Three-song contrast set",
        ("harbor-guitar", "window-piano", "train-guitar-closer"),
        15,
        "corner-cafe",
    )
