"""Debug laboratory for Chapter 13 original-music presentation."""

from open_mic_lab.sample_data import (
    build_sample_repertoire,
    sample_original_presentation_plan,
    sample_setlist,
)
from open_mic_lab.services.originals_service import (
    OriginalMusicAnalysisService,
    OriginalPresentationExperimentService,
)


def run_debug_lab() -> dict[str, object]:
    """Run deterministic debug steps for original-music presentation."""
    repertoire = build_sample_repertoire()
    setlist = sample_setlist()
    plan = sample_original_presentation_plan()
    analyzer = OriginalMusicAnalysisService()
    experiments = OriginalPresentationExperimentService()

    # BREAKPOINT 1: original-work analysis inputs.
    baseline_analysis = analyzer.analyze(plan, setlist, repertoire)
    original_positions = [
        plan.ordered_version_identifiers.index(v) + 1 for v in plan.original_version_identifiers
    ]

    # BREAKPOINT 2: placement evaluation.
    moved_earlier = experiments.move_original_earlier(plan)
    moved_analysis = analyzer.analyze(moved_earlier, setlist, repertoire)

    # BREAKPOINT 3: immutable presentation experiments.
    shortened_story = experiments.shorten_introduction(plan)
    participation_plan = experiments.pair_with_audience_participation(plan)
    immutable_original_order = plan.ordered_version_identifiers
    experiment_order = moved_earlier.ordered_version_identifiers
    original_unchanged = immutable_original_order != experiment_order and plan is not moved_earlier

    # BREAKPOINT 4: comparison of presentation plans.
    comparison = analyzer.compare(plan, moved_earlier, repertoire)

    # BREAKPOINT 5: artistic-identity observations.
    identity = plan.artistic_identity
    identity_observations = (
        f"themes={len(identity.musical_themes)}",
        f"styles={len(identity.recurring_styles)}",
        identity.repertoire_consistency_notes,
    )

    print("Chapter 13 Original Music Debug Lab")
    print(baseline_analysis.summary)
    print(moved_analysis.summary)
    print(f"Original positions: {original_positions}")
    print(f"Original object unchanged: {original_unchanged}")
    print(f"Comparison observations: {len(comparison.differences)}")
    print(f"Identity observations: {identity_observations}")
    print(f"Short story seconds: {shortened_story.introductions[0].duration_seconds}")
    print(f"Participation strategy: {participation_plan.introductions[0].strategy.value}")

    return {
        "observation_count": len(baseline_analysis.observations),
        "opportunity_count": len(baseline_analysis.opportunities),
        "original_positions": tuple(original_positions),
        "original_unchanged": original_unchanged,
        "comparison_count": len(comparison.differences),
        "identity_observations": identity_observations,
    }


if __name__ == "__main__":
    run_debug_lab()
