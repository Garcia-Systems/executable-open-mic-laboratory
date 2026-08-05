"""Debug laboratory for Chapter 4 arrangement experiments.

Place breakpoints on executable lines immediately below each BREAKPOINT marker.
"""

from typing import cast

from open_mic_lab.domain import Arrangement
from open_mic_lab.sample_data import build_sample_repertoire
from open_mic_lab.services.arrangement_service import (
    ArrangementAnalysisService,
    ArrangementComparison,
    ArrangementExperimentService,
    ArrangementTimelineService,
)


def run_lab() -> dict[str, object]:
    """Build deterministic variables for Chapter 4 debugging."""
    repertoire = build_sample_repertoire()
    experiment_service = ArrangementExperimentService()
    analysis_service = ArrangementAnalysisService()
    timeline_service = ArrangementTimelineService()

    # BREAKPOINT: arrangement creation and PerformanceVersion relationship.
    original = repertoire.get_arrangement("window-piano-arrangement")
    source_version = repertoire.get_version(original.source_performance_version_identifier)

    # BREAKPOINT: immutable copying; original remains unchanged.
    transposed = experiment_service.transpose(original, "G", -2)
    immutable_original_key = original.performance_key

    # BREAKPOINT: experiment chaining across several intentional choices.
    simplified = experiment_service.simplify_accompaniment(transposed)
    shortened = experiment_service.shorten_introduction(simplified)
    slowed = experiment_service.alter_tempo(shortened, 64)
    experiment_history = slowed.history

    # BREAKPOINT: arrangement comparison explains tradeoffs without a winner.
    comparison = analysis_service.compare(original, slowed)

    # BREAKPOINT: deterministic timeline generation from arrangement structure.
    timeline = timeline_service.timeline(slowed)
    total_timeline_seconds = sum(entry.duration_seconds for entry in timeline)

    return {
        "repertoire": repertoire,
        "original": original,
        "source_version": source_version,
        "transposed": transposed,
        "immutable_original_key": immutable_original_key,
        "simplified": simplified,
        "shortened": shortened,
        "slowed": slowed,
        "experiment_history": experiment_history,
        "comparison": comparison,
        "timeline": timeline,
        "total_timeline_seconds": total_timeline_seconds,
    }


def main() -> int:
    """Print a concise Chapter 4 debug-lab summary."""
    result = run_lab()
    original = cast(Arrangement, result["original"])
    slowed = cast(Arrangement, result["slowed"])
    comparison = cast(ArrangementComparison, result["comparison"])
    print("Chapter 4 arrangement debug lab")
    print(f"Original: {original.identifier}")
    print(f"Experiment: {slowed.identifier}")
    print(f"History steps: {len(slowed.history)}")
    print(f"Comparison differences: {len(comparison.differences)}")
    print(f"Timeline seconds: {result['total_timeline_seconds']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
