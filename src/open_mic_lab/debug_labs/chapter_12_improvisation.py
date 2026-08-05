"""Debug laboratory for Chapter 12 improvisation decisions.

Set breakpoints on the ``BREAKPOINT`` comments to inspect opportunity detection,
decision analysis, adaptive timeline generation, immutable experiments, and
planned/adapted comparison.
"""

from open_mic_lab.domain import ImprovisationDecision
from open_mic_lab.sample_data import (
    build_sample_repertoire,
    sample_audience_profiles,
    sample_improvisation_context,
)
from open_mic_lab.services.improvisation_service import (
    ImprovisationAnalysisService,
    ImprovisationExperimentService,
)


def run_debug_lab() -> dict[str, object]:
    """Run the Chapter 12 debug scenario and return inspectable values."""
    repertoire = build_sample_repertoire()
    context = sample_improvisation_context()
    arrangement = repertoire.get_arrangement(context.arrangement_identifier)
    audience = sample_audience_profiles()[context.audience_profile_identifier]

    analyzer = ImprovisationAnalysisService()
    experiments = ImprovisationExperimentService()

    report = analyzer.analyze(context, arrangement, audience)  # BREAKPOINT: opportunity detection
    planned = analyzer.planned_timeline(arrangement)  # BREAKPOINT: planned timeline generation
    repeated = experiments.experiment(planned, ImprovisationDecision.REPEAT_CHORUS)
    participation = experiments.experiment(
        repeated, ImprovisationDecision.ADD_AUDIENCE_PARTICIPATION
    )
    adapted = experiments.experiment(
        participation, ImprovisationDecision.EXTEND_ENDING
    )  # BREAKPOINT: immutable improvisation experiments
    comparison = analyzer.compare(planned, adapted)  # BREAKPOINT: planned/adapted comparison

    return {
        "context": context,
        "opportunity_count": len(report.options),
        "planned_duration": planned.total_duration_seconds,
        "adapted_duration": adapted.total_duration_seconds,
        "original_unchanged": planned.identifier != adapted.identifier and not planned.decisions,
        "differences": comparison.differences,
    }


def main() -> None:
    """Print a deterministic debug-lab summary."""
    result = run_debug_lab()
    print("Chapter 12 Improvisation Debug Lab")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
