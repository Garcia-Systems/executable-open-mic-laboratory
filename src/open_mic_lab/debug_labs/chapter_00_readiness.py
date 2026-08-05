"""Chapter 0 debug lab: compare readiness for two versions of one song."""

from dataclasses import dataclass
from decimal import Decimal

from open_mic_lab.domain import PerformanceVersion, PracticeSession, Song
from open_mic_lab.sample_data import build_sample_repertoire, sample_practice_sessions
from open_mic_lab.services.readiness_service import ReadinessResult, calculate_readiness


@dataclass(frozen=True, slots=True)
class Chapter00DebugScenario:
    """Structured state for inspecting a Chapter 0 readiness comparison."""

    song: Song
    original_version: PerformanceVersion
    adapted_version: PerformanceVersion
    practice_sessions: tuple[PracticeSession, ...]
    original_result: ReadinessResult
    adapted_result: ReadinessResult
    original_breakdown: tuple[str, ...]
    adapted_breakdown: tuple[str, ...]
    score_difference: Decimal


def build_debug_scenario() -> Chapter00DebugScenario:
    """Build a deterministic readiness scenario for debugger inspection."""
    repertoire = build_sample_repertoire()
    song = repertoire.get_song("river-road")
    original_version = repertoire.get_version("river-guitar-original")
    adapted_version = repertoire.get_version("river-guitar-lowered")
    practice_sessions = sample_practice_sessions()

    # BREAKPOINT: Inspect the song, original version, adapted version, and practice evidence.
    readiness_inputs = (original_version, adapted_version, practice_sessions)

    # BREAKPOINT: Step Into the real readiness calculation for the original version.
    original_result = calculate_readiness(readiness_inputs[0], readiness_inputs[2])

    # BREAKPOINT: Step Into the real readiness calculation for the adapted version.
    adapted_result = calculate_readiness(readiness_inputs[1], readiness_inputs[2])

    original_breakdown = original_result.breakdown
    adapted_breakdown = adapted_result.breakdown

    # BREAKPOINT: Inspect the two structured breakdowns before comparing scores.
    score_difference = adapted_result.score - original_result.score

    return Chapter00DebugScenario(
        song=song,
        original_version=original_version,
        adapted_version=adapted_version,
        practice_sessions=practice_sessions,
        original_result=original_result,
        adapted_result=adapted_result,
        original_breakdown=original_breakdown,
        adapted_breakdown=adapted_breakdown,
        score_difference=score_difference,
    )


def main() -> None:
    """Run the concise command-line form of the Chapter 0 debug lab."""
    scenario = build_debug_scenario()
    print("Chapter 0 Readiness Debug Lab")
    print(f"Song: {scenario.song.title}")
    print(
        f"Original: {scenario.original_version.identifier} "
        f"{scenario.original_result.score}/100 ({scenario.original_result.category})"
    )
    print(
        f"Adapted: {scenario.adapted_version.identifier} "
        f"{scenario.adapted_result.score}/100 ({scenario.adapted_result.category})"
    )
    print(f"Score difference: {scenario.score_difference:+} points")


if __name__ == "__main__":
    main()
