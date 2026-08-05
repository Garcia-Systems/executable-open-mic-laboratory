"""Debug laboratory for Chapter 10 audience experience."""

from open_mic_lab.sample_data import sample_audience_performance, sample_audience_profiles
from open_mic_lab.services.audience_service import (
    AudienceExperimentService,
    AudienceResponseService,
)


def run_lab() -> dict[str, object]:
    """Run the Chapter 10 debug scenario and return inspectable values."""
    profiles = sample_audience_profiles()
    performance = sample_audience_performance()
    # BREAKPOINT: Inspect audience-profile loading and tendency fields.
    coffeehouse = profiles["supportive-coffeehouse"]
    church = profiles["church-congregation"]
    analyzer = AudienceResponseService()
    experiments = AudienceExperimentService(analyzer)
    # BREAKPOINT: Step Into response analysis for the coffeehouse profile.
    coffeehouse_response = analyzer.analyze(performance, coffeehouse)
    # BREAKPOINT: Step Into response analysis for a different audience profile.
    church_response = analyzer.analyze(performance, church)
    # BREAKPOINT: Compare two audience profiles without producing an audience score.
    comparison = analyzer.compare(performance, coffeehouse, church)
    # BREAKPOINT: Step Into an immutable adaptation experiment.
    familiarity_experiment = experiments.replace_one_unfamiliar_song(performance, church)
    # BREAKPOINT: Confirm the source performance is unchanged after the experiment.
    original_unchanged = performance.identifier == "chapter-10-sample-set"
    changed_is_copy = familiarity_experiment.changed_performance is not performance
    return {
        "profiles": profiles,
        "performance": performance,
        "coffeehouse": coffeehouse,
        "church": church,
        "coffeehouse_response": coffeehouse_response,
        "church_response": church_response,
        "comparison": comparison,
        "familiarity_experiment": familiarity_experiment,
        "original_unchanged": original_unchanged,
        "changed_is_copy": changed_is_copy,
    }


def main() -> None:
    """Print a concise deterministic debug-lab summary."""
    values = run_lab()
    coffeehouse_response = values["coffeehouse_response"]
    church_response = values["church_response"]
    experiment = values["familiarity_experiment"]
    print("Chapter 10 Audience Experience Debug Lab")
    print(f"Coffeehouse strengths: {len(coffeehouse_response.strengths)}")  # type: ignore[attr-defined]
    print(f"Church friction points: {len(church_response.friction_points)}")  # type: ignore[attr-defined]
    print(f"Experiment: {experiment.experiment_name}")  # type: ignore[attr-defined]
    print(f"Original unchanged: {values['original_unchanged']}")
    print(f"Changed is copy: {values['changed_is_copy']}")


if __name__ == "__main__":
    main()
