from open_mic_lab.domain import SetTransition, TransitionEnergyEffect, TransitionKind

# ruff: noqa: E501
from open_mic_lab.sample_data import build_sample_repertoire, sample_setlist, sample_venue
from open_mic_lab.services.set_builder_service import SetBuilderService


def test_timeline_generation_and_cumulative_timing() -> None:
    rep = build_sample_repertoire()
    timeline = SetBuilderService().timeline(sample_setlist(), rep)
    assert [entry.start_time for entry in timeline] == [
        "00:00",
        "00:30",
        "04:00",
        "04:40",
        "08:10",
        "11:35",
    ]
    assert timeline[-1].start_seconds + timeline[-1].duration_seconds == 715


def test_analysis_detects_opener_closer_and_transition_duration() -> None:
    rep = build_sample_repertoire()
    analysis = SetBuilderService().analyze(sample_setlist(), rep, sample_venue())
    assert analysis.fits_venue is True
    assert analysis.total_duration_seconds == 715
    assert any("opener" in strength for strength in analysis.strengths)
    assert any("closer" in strength for strength in analysis.strengths)
    assert any("Transition timing: 01:30" in obs for obs in analysis.observations)


def test_immutable_experiments_and_swap_behavior() -> None:
    service = SetBuilderService()
    original = sample_setlist()
    swapped = service.swap_songs(original, "harbor-guitar", "window-piano")
    assert original.ordered_version_identifiers == (
        "harbor-guitar",
        "window-piano",
        "train-guitar-closer",
    )
    assert swapped.ordered_version_identifiers == (
        "window-piano",
        "harbor-guitar",
        "train-guitar-closer",
    )
    shortened = service.shorten_transition(original, "window-story", 10)
    assert original.transitions[1].estimated_duration_seconds == 40
    assert shortened.transitions[1].estimated_duration_seconds == 30


def test_comparison_service_and_deterministic_energy_ordering() -> None:
    service = SetBuilderService()
    rep = build_sample_repertoire()
    original = sample_setlist()
    energy_order = service.reorder_by_energy(original, rep)
    comparison = service.compare(original, energy_order, rep, sample_venue())
    assert comparison.differences[0].startswith("Duration:")
    assert energy_order.ordered_version_identifiers == (
        "harbor-guitar",
        "window-piano",
        "train-guitar-closer",
    )


def test_insert_transition_is_first_class_object() -> None:
    transition = SetTransition(
        "segue",
        TransitionKind.QUICK_SEGUE,
        12,
        TransitionEnergyEffect.LIFT,
        "Quick segue",
        "harbor-guitar",
    )
    changed = SetBuilderService().insert_transition(sample_setlist(), transition)
    assert changed.transitions[-1] == transition
