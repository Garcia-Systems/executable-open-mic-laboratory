"""Chapter 1 debug lab: compare contextual song suitability and adaptation."""

from dataclasses import dataclass
from decimal import Decimal

from open_mic_lab.domain import PerformanceVersion, Repertoire, SongSelectionProfile, Venue
from open_mic_lab.sample_data import (
    build_sample_repertoire,
    sample_selection_scenarios,
    sample_selection_venue,
)
from open_mic_lab.services.experiment_service import PerformanceVersionExperimentService
from open_mic_lab.services.readiness_service import ReadinessResult, calculate_readiness
from open_mic_lab.services.suitability_service import (
    CandidateComparison,
    SongSuitabilityService,
    SuitabilityResult,
)


@dataclass(frozen=True, slots=True)
class Chapter01DebugScenario:
    """Structured state for inspecting Chapter 1 song suitability decisions."""

    repertoire: Repertoire
    scenario: SongSelectionProfile
    venue: Venue
    candidate_a: PerformanceVersion
    candidate_b: PerformanceVersion
    candidate_b_original_key: str
    candidate_a_readiness: ReadinessResult
    candidate_b_readiness: ReadinessResult
    candidate_a_result: SuitabilityResult
    candidate_b_result: SuitabilityResult
    adapted_candidate_b: PerformanceVersion
    adapted_candidate_b_result: SuitabilityResult
    comparison: CandidateComparison
    adapted_comparison: CandidateComparison
    source_candidate_was_mutated: bool
    score_change: Decimal


def build_debug_scenario() -> Chapter01DebugScenario:
    """Build a deterministic contextual suitability scenario for debugger inspection."""
    repertoire = build_sample_repertoire()
    scenarios = sample_selection_scenarios()
    scenario = scenarios["coffeehouse"]
    venue = sample_selection_venue(scenario.venue_identifier)
    service = SongSuitabilityService()
    experiments = PerformanceVersionExperimentService()

    candidate_a = repertoire.get_version("harbor-guitar")
    candidate_b = repertoire.get_version("window-guitar-original-feature")
    candidate_b_original_key = candidate_b.performance_key

    # BREAKPOINT: Inspect the profile, hard constraints, soft preferences, weights, and candidates.
    candidates = (candidate_a, candidate_b)

    candidate_a_readiness = calculate_readiness(candidate_a)
    candidate_b_readiness = calculate_readiness(candidate_b)

    # BREAKPOINT: Step Into the suitability service for Candidate A.
    candidate_a_result = service.evaluate(
        candidates[0], repertoire, scenario, venue, candidate_a_readiness
    )

    # BREAKPOINT: Step Into the suitability service for Candidate B and inspect criteria.
    candidate_b_result = service.evaluate(
        candidates[1], repertoire, scenario, venue, candidate_b_readiness
    )

    # BREAKPOINT: Inspect stable ranking and tie-breaking in the comparison result.
    comparison = service.compare(candidates, repertoire, scenario, venue)

    # BREAKPOINT: Step Into the experiment service and confirm it returns a copied version.
    adapted_candidate_b = experiments.transpose(candidate_b, "F", -2)

    # BREAKPOINT: Confirm the source object is unchanged, then reevaluate the adapted copy.
    adapted_candidate_b_result = service.evaluate(adapted_candidate_b, repertoire, scenario, venue)
    repertoire.add_performance_version(adapted_candidate_b)

    adapted_comparison = service.compare(
        (candidate_a, adapted_candidate_b), repertoire, scenario, venue
    )
    source_candidate_was_mutated = candidate_b.performance_key != candidate_b_original_key
    score_change = adapted_candidate_b_result.score - candidate_b_result.score

    return Chapter01DebugScenario(
        repertoire=repertoire,
        scenario=scenario,
        venue=venue,
        candidate_a=candidate_a,
        candidate_b=candidate_b,
        candidate_b_original_key=candidate_b_original_key,
        candidate_a_readiness=candidate_a_readiness,
        candidate_b_readiness=candidate_b_readiness,
        candidate_a_result=candidate_a_result,
        candidate_b_result=candidate_b_result,
        adapted_candidate_b=adapted_candidate_b,
        adapted_candidate_b_result=adapted_candidate_b_result,
        comparison=comparison,
        adapted_comparison=adapted_comparison,
        source_candidate_was_mutated=source_candidate_was_mutated,
        score_change=score_change,
    )


def main() -> None:
    """Run the concise command-line form of the Chapter 1 debug lab."""
    lab = build_debug_scenario()
    print("Chapter 1 Song Suitability Debug Lab")
    print(f"Scenario: {lab.scenario.name}")
    print(f"Candidate A: {lab.candidate_a.identifier} {lab.candidate_a_result.score}/100")
    print(f"Candidate B: {lab.candidate_b.identifier} {lab.candidate_b_result.score}/100")
    print(
        f"Adapted B: {lab.adapted_candidate_b.identifier} "
        f"{lab.adapted_candidate_b_result.score}/100 ({lab.score_change:+})"
    )
    print("Ranking: " + ", ".join(result.version_id for result in lab.comparison.results))


if __name__ == "__main__":
    main()
