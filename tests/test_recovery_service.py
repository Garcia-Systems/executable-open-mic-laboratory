from dataclasses import FrozenInstanceError

import pytest

from open_mic_lab.domain import IncidentType, PerformanceIncident, RecoveryStage, RecoveryStrategy
from open_mic_lab.sample_data import sample_recovery_scenario
from open_mic_lab.services.recovery_service import (
    IncidentCatalogService,
    RecoveryAnalysisService,
    RecoveryExperimentService,
)


def test_incident_catalog_contains_educational_scenarios() -> None:
    incidents = IncidentCatalogService().list_incidents()
    assert len(incidents) == 11
    assert {i.incident_type for i in incidents} >= {
        IncidentType.FORGOTTEN_LYRICS,
        IncidentType.WRONG_CHORD,
        IncidentType.AUDIENCE_INTERRUPTION,
    }


def test_incident_model_is_immutable_and_validated() -> None:
    incident = IncidentCatalogService().get("forgotten-lyrics")
    with pytest.raises(FrozenInstanceError):
        incident.description = "changed"  # type: ignore[misc]
    with pytest.raises(ValueError):
        PerformanceIncident("bad", IncidentType.WRONG_CHORD, "chorus", "bad", 11, 1)


def test_recovery_analysis_has_no_mistake_score() -> None:
    report = RecoveryAnalysisService().analyze(sample_recovery_scenario())
    assert report.observations
    assert report.outcomes
    assert not hasattr(report, "score")
    assert any("Continuing confidently" in item for item in report.observations)


def test_timeline_is_deterministic() -> None:
    service = RecoveryAnalysisService()
    first = service.timeline(sample_recovery_scenario())
    second = service.timeline(sample_recovery_scenario())
    assert first == second
    assert tuple(event.stage for event in first.events) == (
        RecoveryStage.MISTAKE_OCCURS,
        RecoveryStage.PERFORMER_RECOGNIZES,
        RecoveryStage.RECOVERY_DECISION,
        RecoveryStage.AUDIENCE_PERCEPTION,
        RecoveryStage.PERFORMANCE_CONTINUES,
        RecoveryStage.REFLECTION,
    )


def test_recovery_experiments_are_immutable() -> None:
    scenario = sample_recovery_scenario()
    changed = RecoveryExperimentService().with_strategy(scenario, RecoveryStrategy.RESTART_SECTION)
    assert scenario.preferred_strategy is RecoveryStrategy.CONTINUE_IMMEDIATELY
    assert changed.preferred_strategy is RecoveryStrategy.RESTART_SECTION
    assert changed.experiment_history == ("strategy: restart section",)


def test_comparison_service_reports_tradeoffs() -> None:
    scenario = sample_recovery_scenario()
    experiments = RecoveryExperimentService()
    comparison = RecoveryAnalysisService().compare(
        experiments.with_strategy(scenario, RecoveryStrategy.CONTINUE_IMMEDIATELY),
        experiments.with_strategy(scenario, RecoveryStrategy.RESTART_SECTION),
    )
    assert comparison.different_tradeoffs
    assert comparison.reflection_prompts
