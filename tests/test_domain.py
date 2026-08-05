from decimal import Decimal

import pytest

from open_mic_lab.domain import (
    Difficulty,
    Genre,
    Instrument,
    Mood,
    PerformanceStatus,
    PerformanceVersion,
    SetList,
    Song,
)
from open_mic_lab.sample_data import build_sample_repertoire


def test_song_rejects_invalid_tempo() -> None:
    with pytest.raises(ValueError, match="Original tempo must be positive"):
        Song(
            "bad",
            "Bad",
            "Nobody",
            Genre.FOLK,
            "C",
            0,
            "4/4",
            Mood.WARM,
            Decimal("5"),
            Decimal("5"),
            Decimal("5"),
        )


def test_performance_version_rejects_invalid_rating() -> None:
    with pytest.raises(ValueError, match="Vocal comfort must be between 0 and 10"):
        PerformanceVersion(
            "v",
            "s",
            "C",
            100,
            Instrument.GUITAR_VOCAL,
            Difficulty.SIMPLE,
            Decimal("11"),
            Decimal("5"),
            Decimal("5"),
            Decimal("5"),
            PerformanceStatus.IDEA,
            0,
        )


def test_repertoire_rejects_duplicates_and_unknown_song() -> None:
    rep = build_sample_repertoire()
    with pytest.raises(ValueError, match="already exists"):
        rep.add_song(rep.get_song("river-road"))
    unknown = PerformanceVersion(
        "unknown",
        "missing",
        "C",
        90,
        Instrument.GUITAR_VOCAL,
        Difficulty.SIMPLE,
        Decimal("5"),
        Decimal("5"),
        Decimal("5"),
        Decimal("5"),
        PerformanceStatus.IDEA,
        0,
    )
    with pytest.raises(ValueError, match="unknown song"):
        rep.add_performance_version(unknown)


def test_setlist_rejects_duplicate_versions() -> None:
    with pytest.raises(ValueError, match="cannot repeat"):
        SetList("s", "Set", ("a", "a"), 10, "venue")


def test_filters_and_ready_versions() -> None:
    rep = build_sample_repertoire()
    assert {v.identifier for v in rep.list_ready_versions()} == {
        "harbor-guitar",
        "train-guitar-closer",
    }
    assert rep.filter_by_genre(Genre.ORIGINAL)[0].identifier == "window-piano"
    assert rep.filter_by_instrument(Instrument.PIANO_VOCAL)
    assert rep.filter_by_mood(Mood.ENERGETIC)[0].identifier == "train-guitar-closer"
