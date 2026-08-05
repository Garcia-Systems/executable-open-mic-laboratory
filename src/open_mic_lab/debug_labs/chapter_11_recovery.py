"""Debug laboratory for Chapter 11 recovery from mistakes."""

from open_mic_lab.domain import RecoveryStrategy, RecoveryTimeline
from open_mic_lab.sample_data import sample_recovery_scenario
from open_mic_lab.services.recovery_service import (
    RecoveryAnalysisService,
    RecoveryExperimentService,
)


def build_debug_recovery_story() -> dict[str, object]:
    """Build meaningful variables for debugging recovery decisions."""
    analyzer = RecoveryAnalysisService()
    experiments = RecoveryExperimentService()

    # BREAKPOINT: Inspect incident creation and the sample performance context.
    scenario = sample_recovery_scenario()

    # BREAKPOINT: Step Into deterministic recovery analysis; confirm no mistake score exists.
    immediate_report = analyzer.analyze(scenario)

    # BREAKPOINT: Inspect immutable recovery experiments and verify original scenario is unchanged.
    restart = experiments.with_strategy(scenario, RecoveryStrategy.RESTART_SECTION)
    simplified = experiments.with_strategy(scenario, RecoveryStrategy.SIMPLIFY_ACCOMPANIMENT)
    restart_report = analyzer.analyze(restart)
    simplified_report = analyzer.analyze(simplified)

    # BREAKPOINT: Compare strategy tradeoffs as educational observations, not universal rules.
    comparison = analyzer.compare(restart, simplified)

    # BREAKPOINT: Inspect timeline generation from mistake through reflection.
    timeline = analyzer.timeline(restart)

    return {
        "scenario": scenario,
        "immediate_report": immediate_report,
        "restart_report": restart_report,
        "simplified_report": simplified_report,
        "comparison": comparison,
        "timeline": timeline,
        "original_strategy": scenario.preferred_strategy,
    }


def main() -> None:
    """Run the Chapter 11 debug laboratory."""
    story = build_debug_recovery_story()
    timeline = story["timeline"]
    if not isinstance(timeline, RecoveryTimeline):
        raise TypeError("Expected a RecoveryTimeline in the debug story.")
    print("Chapter 11 Recovery Debug Lab")
    print(f"Original strategy: {sample_recovery_scenario().preferred_strategy.value}")
    for event in timeline.events:
        print(f"{event.stage.value} -> {event.note}")


if __name__ == "__main__":
    main()
