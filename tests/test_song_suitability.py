from dataclasses import replace
from decimal import Decimal

import pytest

from open_mic_lab.domain import Difficulty, VocalNote, VocalRange
from open_mic_lab.sample_data import (
    build_sample_repertoire,
    sample_selection_scenarios,
    sample_selection_venue,
)
from open_mic_lab.services.experiment_service import PerformanceVersionExperimentService
from open_mic_lab.services.suitability_service import DEFAULT_WEIGHTS, SongSuitabilityService


def test_vocal_note_and_range_behavior() -> None:
    assert VocalNote.parse("Bb4").pitch_number == VocalNote.parse("A#4").pitch_number
    assert VocalNote.parse("C3") < VocalNote.parse("F#3")
    with pytest.raises(ValueError):
        VocalNote.parse("H2")
    comfort = VocalRange.from_strings("A2", "D4")
    required = VocalRange.from_strings("Bb2", "C#4")
    assert comfort.contains(required)
    outside = VocalRange.from_strings("G2", "E4")
    assert comfort.outside_distance(outside) == 4
    assert str(required.transpose(-2)) == "G#2-B3"


def test_suitability_scoring_boundaries_missing_and_weights() -> None:
    rep = build_sample_repertoire()
    profile = sample_selection_scenarios()["coffeehouse"]
    venue = sample_selection_venue(profile.venue_identifier)
    service = SongSuitabilityService()
    result = service.evaluate(rep.get_version("harbor-guitar"), rep, profile, venue)
    assert Decimal("0") <= result.score <= Decimal("100")
    assert result.completeness < Decimal("100")
    assert "neutral score" in " ".join(c.explanation for c in result.criteria)
    with pytest.raises(ValueError):
        bad = {**DEFAULT_WEIGHTS, "vocal": Decimal("-1")}
        service.evaluate(
            rep.get_version("harbor-guitar"), rep, replace(profile, weights=bad), venue
        )


def test_hard_constraints_and_fit_effects() -> None:
    rep = build_sample_repertoire()
    profile = sample_selection_scenarios()["first-performance"]
    venue = sample_selection_venue(profile.venue_identifier)
    service = SongSuitabilityService()
    risky = service.evaluate(rep.get_version("window-guitar-original-feature"), rep, profile, venue)
    safe = service.evaluate(rep.get_version("train-guitar-closer"), rep, profile, venue)
    assert risky.hard_constraints
    assert safe.score > risky.score
    assert any(c.name == "audience" for c in safe.criteria)
    assert any(c.name == "connection" for c in risky.criteria)


def test_comparison_determinism_filtering_and_empty() -> None:
    rep = build_sample_repertoire()
    profile = sample_selection_scenarios()["first-performance"]
    venue = sample_selection_venue(profile.venue_identifier)
    service = SongSuitabilityService()
    subset = (rep.get_version("window-guitar-original-feature"), rep.get_version("harbor-guitar"))
    first = service.compare(subset, rep, profile, venue)
    second = service.compare(subset, rep, profile, venue)
    assert [r.version_id for r in first.results] == [r.version_id for r in second.results]
    filtered = service.compare(subset, rep, profile, venue, include_constrained=False)
    assert filtered.excluded
    assert all(not r.hard_constraints for r in filtered.results)
    assert "No candidate" in service.compare((), rep, profile, venue).observations[0]
    assert first.observations


def test_experiments_copy_and_can_change_suitability() -> None:
    rep = build_sample_repertoire()
    version = rep.get_version("window-guitar-original-feature")
    experiments = PerformanceVersionExperimentService()
    lowered = experiments.transpose(version, "F", -2)
    simplified = experiments.simplify(version)
    assert version.performance_key == "G"
    assert lowered.performance_key == "F"
    assert str(lowered.required_vocal_range) == "A2-D#4"
    assert simplified.identifier.endswith("simplified")
    assert simplified.arrangement_difficulty == Difficulty.MODERATE
    assert simplified.accompaniment_stability <= Decimal("10")
    assert simplified.adaptation_notes
    profile = sample_selection_scenarios()["coffeehouse"]
    venue = sample_selection_venue(profile.venue_identifier)
    service = SongSuitabilityService()
    assert (
        service.evaluate(lowered, rep, profile, venue).criteria[0].score
        > service.evaluate(version, rep, profile, venue).criteria[0].score
    )
