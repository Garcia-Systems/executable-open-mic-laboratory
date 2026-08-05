"""Debug laboratory for Chapter 5 coordination models."""

from open_mic_lab.domain import CoordinationExperiment
from open_mic_lab.sample_data import sample_coordination_profile
from open_mic_lab.services.coordination_service import (
    CoordinationAnalysisService,
    CoordinationExperimentService,
    TempoLadderService,
)

BREAKPOINT_MARKERS = (
    "coordination-score calculation",
    "tempo ladder generation",
    "bottleneck identification",
    "practice experiment effects",
    "immutable experiment copies",
)


def run_debug_lab() -> dict[str, object]:
    """Return meaningful variables for debugger inspection."""
    profile = sample_coordination_profile()
    baseline = CoordinationExperiment(profile)
    analyzer = CoordinationAnalysisService()
    experiments = CoordinationExperimentService()

    baseline_analysis = analyzer.analyze(baseline.profile)  # breakpoint: coordination score
    bottlenecks = analyzer.bottlenecks(baseline.profile)  # breakpoint: bottlenecks
    simplified = experiments.simplify_accompaniment(baseline)  # breakpoint: immutable copy
    tempo_experiment = experiments.reduce_tempo(baseline, 60)  # breakpoint: tempo effect
    simplified_analysis = analyzer.analyze(simplified.profile)
    tempo_analysis = analyzer.analyze(tempo_experiment.profile)
    ladder = TempoLadderService().generate(60, profile.target_tempo_bpm, 6)  # breakpoint: ladder

    return {
        "markers": BREAKPOINT_MARKERS,
        "baseline_score": baseline_analysis.coordination_score,
        "simplified_score": simplified_analysis.coordination_score,
        "tempo_score": tempo_analysis.coordination_score,
        "baseline_load": baseline_analysis.cognitive_load.score,
        "simplified_load": simplified_analysis.cognitive_load.score,
        "bottlenecks": bottlenecks,
        "ladder": ladder.tempos,
        "original_identifier": baseline.profile.identifier,
        "simplified_identifier": simplified.profile.identifier,
        "original_unchanged": baseline.profile.identifier == profile.identifier,
    }


def main() -> int:
    """Print the Chapter 5 debug laboratory snapshot."""
    snapshot = run_debug_lab()
    print("Chapter 5 coordination debug laboratory")
    for key, value in snapshot.items():
        print(f"{key}: {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
