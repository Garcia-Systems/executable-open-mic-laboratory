"""Tests for Chapter 14 event orchestration."""

from open_mic_lab.domain import EventScenario
from open_mic_lab.sample_data import build_sample_repertoire
from open_mic_lab.services.event_service import OpenMicEventService


def test_event_simulation_is_deterministic() -> None:
    rep = build_sample_repertoire()
    service = OpenMicEventService()

    left = service.simulate(rep)
    right = service.simulate(rep)

    assert left == right
    assert [entry.label for entry in left.timeline.entries] == [
        "Arrive",
        "Sign Up",
        "Observe Other Performers",
        "Sound Check",
        "Called to Stage",
        "Introduction",
        "Performance Begins",
        "Performance Ends",
        "Networking",
        "Reflection",
    ]


def test_event_report_references_all_subsystems() -> None:
    rep = build_sample_repertoire()
    service = OpenMicEventService()
    event = service.simulate(rep)

    report = service.report(rep, event)

    assert report.preparation
    assert report.repertoire_used == event.slot.version_identifiers
    assert report.arrangement_choices
    assert report.communication_plan
    assert report.equipment_setup
    assert report.soundcheck_observations
    assert report.audience_observations
    assert report.recovery_events
    assert report.improvisation_opportunities
    assert report.original_music_notes
    assert report.reflection_prompts


def test_event_experiments_are_immutable() -> None:
    rep = build_sample_repertoire()
    service = OpenMicEventService()
    event = service.simulate(rep)

    changed = service.experiment(event, "delayed-performance-slot")
    recovery = service.experiment(event, "unexpected-recovery-event")

    assert event.experiment_history == ()
    assert changed.experiment_history == ("delayed-performance-slot",)
    assert changed.slot.call_time == "19:45"
    assert event.slot.call_time == "19:20"
    assert "cable-disconnected" in recovery.execution.recovery_event


def test_event_compare_and_mermaid() -> None:
    rep = build_sample_repertoire()
    service = OpenMicEventService()
    first = service.simulate(rep)
    showcase = service.simulate(rep, EventScenario.SONGWRITER_SHOWCASE, "church")

    assert "flowchart TD" in service.mermaid(first)
    assert any("scenario:" in line for line in service.compare(first, showcase))
