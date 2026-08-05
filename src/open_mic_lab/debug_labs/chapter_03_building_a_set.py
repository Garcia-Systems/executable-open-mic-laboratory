"""Debug laboratory for Chapter 3 — Building a Set.

Suggested breakpoint locations are the executable lines immediately below each
``BREAKPOINT:`` marker. Inspect the named variables to understand the complete
set-analysis pipeline and the immutability of experiments.
"""

from typing import cast

from open_mic_lab.domain import SetList
from open_mic_lab.sample_data import build_sample_repertoire, sample_set_scenarios, sample_venue
from open_mic_lab.services.set_builder_service import SetBuilderService, SetFlowAnalysis


def run_lab() -> dict[str, object]:
    """Run the deterministic Chapter 3 debug scenario."""
    # BREAKPOINT: loading a candidate set
    repertoire = build_sample_repertoire()
    scenarios = sample_set_scenarios()
    candidate_set = scenarios["coffeehouse-15"]
    comparison_set = scenarios["listening-room"]
    venue = sample_venue()
    service = SetBuilderService()

    # BREAKPOINT: transition generation
    transitions = candidate_set.transitions

    # BREAKPOINT: cumulative timing and timeline construction
    timeline = service.timeline(candidate_set, repertoire)
    cumulative_running_time = timeline[-1].start_seconds + timeline[-1].duration_seconds

    # BREAKPOINT: energy analysis
    analysis = service.analyze(candidate_set, repertoire, venue)
    energy_observation = next(obs for obs in analysis.observations if obs.startswith("Energy"))

    # BREAKPOINT: comparison of two sets
    comparison = service.compare(candidate_set, comparison_set, repertoire, venue)

    # BREAKPOINT: immutable set experiments
    swapped_set = service.swap_songs(candidate_set, "harbor-guitar", "window-piano")
    immutable_original_order = candidate_set.ordered_version_identifiers
    experiment_order = swapped_set.ordered_version_identifiers

    return {
        "repertoire": repertoire,
        "candidate_set": candidate_set,
        "transitions": transitions,
        "timeline": timeline,
        "cumulative_running_time": cumulative_running_time,
        "analysis": analysis,
        "energy_observation": energy_observation,
        "comparison": comparison,
        "swapped_set": swapped_set,
        "immutable_original_order": immutable_original_order,
        "experiment_order": experiment_order,
    }


def main() -> None:
    """Print a compact deterministic debug-lab summary."""
    result = run_lab()
    analysis = cast(SetFlowAnalysis, result["analysis"])
    candidate_set = cast(SetList, result["candidate_set"])
    print("Chapter 3 Building a Set Debug Lab")
    print(f"Set: {candidate_set.name}")
    print(f"Timeline entries: {len(result['timeline'])}")  # type: ignore[arg-type]
    print(f"Cumulative seconds: {result['cumulative_running_time']}")
    print(f"Assessment: {analysis.overall_assessment}")
    print(f"Immutable experiment order: {result['experiment_order']}")


if __name__ == "__main__":
    main()
