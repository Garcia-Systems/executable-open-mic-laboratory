"""Debug lab for Chapter 9 Sound Check Laboratory.

Place breakpoints on executable lines immediately after BREAKPOINT markers.
"""

from typing import cast

from open_mic_lab.domain.soundcheck import VenueAcoustics
from open_mic_lab.equipment_templates import piano_and_vocal_setup
from open_mic_lab.services.soundcheck_service import (
    SoundCheckAnalysis,
    SoundCheckComparison,
    SoundCheckExperimentService,
    SoundCheckService,
)
from open_mic_lab.soundcheck_templates import sample_soundcheck, venue_profiles


def run_lab() -> dict[str, object]:
    """Run deterministic sound-check scenarios for debugger inspection."""
    # BREAKPOINT: inspect venue-profile loading.
    venues = venue_profiles()
    venue = venues["noisy-cafe"]

    # BREAKPOINT: inspect equipment setup and baseline mixer settings.
    setup = piano_and_vocal_setup()
    soundcheck = sample_soundcheck(venue.identifier)

    service = SoundCheckService()
    experiments = SoundCheckExperimentService()

    # BREAKPOINT: step into mixer analysis and balance calculations.
    baseline_analysis = service.analyze(soundcheck, setup)

    # BREAKPOINT: inspect repeatable workflow observations.
    workflow = service.workflow(soundcheck, setup)

    # BREAKPOINT: confirm immutable monitor experiment.
    raised_monitor = experiments.change_monitor(soundcheck, 2)
    monitor_analysis = service.analyze(raised_monitor, setup)
    immutable_original_monitor = soundcheck.mixer_settings.monitor_mix.overall_level

    # BREAKPOINT: compare two mixes without declaring a perfect answer.
    comparison = service.compare(soundcheck, raised_monitor, setup)

    # BREAKPOINT: inspect gain, EQ, microphone-distance, and mute experiments.
    louder_vocal = experiments.change_gain(soundcheck, "ch1", 1)
    closer_mic = experiments.move_microphone(soundcheck, "ch1", -5)
    muted_piano = experiments.mute_channel(soundcheck, "ch2")

    return {
        "venues": venues,
        "venue": venue,
        "setup": setup,
        "soundcheck": soundcheck,
        "baseline_analysis": baseline_analysis,
        "workflow": workflow,
        "raised_monitor": raised_monitor,
        "monitor_analysis": monitor_analysis,
        "immutable_original_monitor": immutable_original_monitor,
        "comparison": comparison,
        "louder_vocal": louder_vocal,
        "closer_mic": closer_mic,
        "muted_piano": muted_piano,
    }


if __name__ == "__main__":
    result = run_lab()
    venue = cast(VenueAcoustics, result["venue"])
    analysis = cast(SoundCheckAnalysis, result["baseline_analysis"])
    comparison = cast(SoundCheckComparison, result["comparison"])
    print("Chapter 9 Sound Check Debug Lab")
    print(f"Venue: {venue.name}")
    print(f"Baseline feedback risk: {analysis.feedback_risk.value}")
    for difference in comparison.differences:
        print(f"Difference: {difference}")
