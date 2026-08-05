from dataclasses import FrozenInstanceError

from open_mic_lab.sample_data import sample_communication_plan
from open_mic_lab.services.stage_service import (
    CommunicationAnalysisService,
    CommunicationExperimentService,
)


def test_communication_analysis_is_transparent_and_deterministic() -> None:
    plan = sample_communication_plan()
    service = CommunicationAnalysisService()
    first = service.analyze(plan)
    second = service.analyze(plan)
    assert first == second
    assert "stage presence score" not in first.summary.lower()
    assert any("Long silence" in item for item in first.observations)
    assert first.suggested_experiments


def test_introduction_timing_flags_long_story() -> None:
    plan = sample_communication_plan()
    observations = CommunicationAnalysisService().analyze_introductions(plan)
    assert any("Song 2" in item and "slow pacing" in item for item in observations)


def test_flow_evaluation_includes_recovery_and_eye_contact() -> None:
    plan = sample_communication_plan()
    observations = CommunicationAnalysisService().analyze_flow(plan)
    assert any("Eye-contact" in item for item in observations)
    assert any("recovery breath" in item for item in observations)


def test_experiments_are_immutable() -> None:
    plan = sample_communication_plan()
    changed = CommunicationExperimentService().shorten_introduction(plan, "intro-window")
    assert changed is not plan
    assert changed.planned_spoken_seconds < plan.planned_spoken_seconds
    assert plan.identifier == "chapter-seven-baseline"
    try:
        plan.identifier = "mutated"  # type: ignore[misc]
    except FrozenInstanceError:
        pass
    else:  # pragma: no cover
        raise AssertionError("CommunicationPlan should be frozen")


def test_compare_reports_tradeoffs() -> None:
    plan = sample_communication_plan()
    experiments = CommunicationExperimentService()
    changed = experiments.invite_audience_participation(
        experiments.shorten_introduction(plan, "intro-window")
    )
    comparison = CommunicationAnalysisService().compare(plan, changed)
    assert comparison.differences == (
        "Spoken time changed from 109 to 109 seconds.",
        "Interaction count changed from 1 to 2.",
        "Observation count changed from 7 to 7.",
    )
