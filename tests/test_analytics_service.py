import pytest

from open_mic_lab.domain import PerformanceHistory
from open_mic_lab.sample_data import sample_performance_history
from open_mic_lab.services.analytics_service import (
    ImprovementExperimentService,
    PerformanceAnalyticsService,
)


def test_analytics_report_is_deterministic() -> None:
    service = PerformanceAnalyticsService()
    left = service.report(sample_performance_history())
    right = service.report(sample_performance_history())
    assert left == right
    assert left.dashboard.text.startswith("Performance Dashboard")
    assert "History" in left.dashboard.mermaid


def test_trends_and_recommendations_explain_evidence() -> None:
    service = PerformanceAnalyticsService()
    report = service.report(sample_performance_history())
    assert any(trend.name == "Readiness over time" for trend in report.trends)
    assert all(recommendation.reason for recommendation in report.recommendations)
    assert any(
        "closing" in recommendation.action.lower() for recommendation in report.recommendations
    )


def test_improvement_experiments_are_immutable() -> None:
    service = PerformanceAnalyticsService()
    experiments = ImprovementExperimentService()
    baseline = service.improvement_plan(sample_performance_history())
    changed = experiments.emphasize_practice(baseline)
    assert baseline.focus == "balanced"
    assert baseline.experiment_history == ()
    assert changed.focus == "practice emphasis"
    assert changed.actions[0].startswith("Schedule")


def test_history_requires_chronological_snapshots() -> None:
    history = sample_performance_history()
    with pytest.raises(ValueError, match="chronological"):
        PerformanceHistory(tuple(reversed(history.snapshots)))
