"""Debug laboratory for Chapter 15 performance analytics."""

from open_mic_lab.sample_data import sample_performance_history
from open_mic_lab.services.analytics_service import (
    ImprovementExperimentService,
    PerformanceAnalyticsService,
)


def run_debug_lab() -> dict[str, object]:
    """Run deterministic debug checkpoints for analytics and planning."""
    # BREAKPOINT 1: history aggregation from simulated performances.
    history = sample_performance_history()
    latest_snapshot = history.snapshots[-1]

    analytics = PerformanceAnalyticsService()
    experiments = ImprovementExperimentService()

    # BREAKPOINT 2: analytics generation from chronological snapshots.
    trends = analytics.trends(history)
    practice_trend = analytics.practice_trend(history)
    repertoire_trend = analytics.repertoire_trend(history)

    # BREAKPOINT 3: recommendation engine with transparent reasons.
    recommendations = analytics.recommendations(history)

    # BREAKPOINT 4: dashboard creation from trend values.
    dashboard = analytics.dashboard(history)

    # BREAKPOINT 5: immutable improvement experiments.
    baseline_plan = analytics.improvement_plan(history)
    practice_plan = experiments.emphasize_practice(baseline_plan)
    technical_plan = experiments.technical_focus_month(baseline_plan)
    comparison = experiments.compare(practice_plan, technical_plan)
    baseline_unchanged = baseline_plan.focus == "balanced" and not baseline_plan.experiment_history

    return {
        "history": history,
        "latest_snapshot": latest_snapshot,
        "trends": trends,
        "practice_trend": practice_trend,
        "repertoire_trend": repertoire_trend,
        "recommendations": recommendations,
        "dashboard": dashboard,
        "baseline_plan": baseline_plan,
        "practice_plan": practice_plan,
        "technical_plan": technical_plan,
        "comparison": comparison,
        "baseline_unchanged": baseline_unchanged,
    }


def main() -> None:
    """Print a compact debug-lab summary."""
    data = run_debug_lab()
    history = data["history"]
    dashboard = data["dashboard"]
    recommendations = data["recommendations"]
    print("Chapter 15 debug lab: performance analytics")
    print(f"Snapshots: {len(history.snapshots)}")  # type: ignore[attr-defined]
    print(dashboard.text)  # type: ignore[attr-defined]
    print(f"Recommendations: {len(recommendations)}")  # type: ignore[arg-type]
    print(f"Baseline unchanged: {data['baseline_unchanged']}")


if __name__ == "__main__":
    main()
