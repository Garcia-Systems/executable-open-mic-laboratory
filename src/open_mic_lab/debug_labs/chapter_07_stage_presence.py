"""Debug laboratory for Chapter 7 stage-presence communication."""

from open_mic_lab.sample_data import sample_communication_plan
from open_mic_lab.services.stage_service import (
    CommunicationAnalysisService,
    CommunicationExperimentService,
)


def run_lab() -> None:
    """Run a deterministic debugging path through the communication engine."""
    # BREAKPOINT 1: Inspect communication-plan construction.
    plan = sample_communication_plan()
    analysis_service = CommunicationAnalysisService()
    experiment_service = CommunicationExperimentService()

    # BREAKPOINT 2: Step into introduction analysis and inspect timing tradeoffs.
    introduction_observations = analysis_service.analyze_introductions(plan)

    # BREAKPOINT 3: Step into pacing evaluation and audience interaction analysis.
    flow_observations = analysis_service.analyze_flow(plan)
    baseline_analysis = analysis_service.analyze(plan)

    # BREAKPOINT 4: Verify experiments return new plans without mutating the original.
    shortened_plan = experiment_service.shorten_introduction(plan, "intro-window")
    participation_plan = experiment_service.invite_audience_participation(shortened_plan)

    # BREAKPOINT 5: Compare flow before and after communication changes.
    comparison = analysis_service.compare(plan, participation_plan)
    print("Chapter 7 Debug Lab — Stage Presence")
    print(f"Plan: {plan.identifier} ({plan.planned_spoken_seconds}s planned)")
    print(f"Introduction observations: {len(introduction_observations)}")
    print(f"Flow observations: {len(flow_observations)}")
    print(f"Baseline summary: {baseline_analysis.summary}")
    print(
        "Changed plan: "
        f"{participation_plan.identifier} ({participation_plan.planned_spoken_seconds}s)"
    )
    for difference in comparison.differences:
        print(f"Difference: {difference}")
    print(f"Original object unchanged: {plan.identifier == 'chapter-seven-baseline'}")


if __name__ == "__main__":
    run_lab()
