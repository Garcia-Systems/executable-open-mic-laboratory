from dataclasses import replace

from open_mic_lab.domain.soundcheck import BalanceAssessment, EQProfile, FeedbackRisk
from open_mic_lab.equipment_templates import piano_and_vocal_setup
from open_mic_lab.services.soundcheck_service import SoundCheckExperimentService, SoundCheckService
from open_mic_lab.soundcheck_templates import sample_soundcheck, venue_profiles


def test_venue_profiles_are_deterministic_and_educational():
    profiles = venue_profiles()
    assert tuple(profiles) == (
        "quiet-coffeehouse",
        "noisy-cafe",
        "church-sanctuary",
        "outdoor-event",
        "rehearsal-room",
        "community-center",
    )
    assert (
        "educational"
        in SoundCheckService().analyze(sample_soundcheck(), piano_and_vocal_setup()).observations[0]
    )


def test_soundcheck_analysis_reports_balance_and_risks():
    analysis = SoundCheckService().analyze(sample_soundcheck(), piano_and_vocal_setup())
    assert analysis.vocal_balance is BalanceAssessment.BALANCED
    assert analysis.monitor_balance is BalanceAssessment.SLIGHTLY_QUIET
    assert analysis.feedback_risk in {FeedbackRisk.LOW, FeedbackRisk.MODERATE, FeedbackRisk.HIGH}
    assert "ch3" in analysis.unused_channels
    assert analysis.suggested_adjustments
    assert analysis.strengths


def test_workflow_has_repeatable_steps():
    workflow = SoundCheckService().workflow(sample_soundcheck(), piano_and_vocal_setup())
    assert [step.number for step in workflow] == [1, 2, 3, 4, 5, 6, 7]
    assert workflow[0].name == "verify signal path"
    assert workflow[-1].name == "confirm performer comfort"


def test_experiments_are_immutable():
    original = sample_soundcheck()
    changed = SoundCheckExperimentService().change_monitor(original, 2)
    assert original is not changed
    assert original.mixer_settings.monitor_mix.overall_level == 3
    assert changed.mixer_settings.monitor_mix.overall_level == 5
    assert changed.identifier.endswith("monitor-+2")


def test_gain_eq_distance_and_mute_experiments():
    original = sample_soundcheck()
    experiments = SoundCheckExperimentService()
    louder = experiments.change_gain(original, "ch1", 2)
    eq = experiments.adjust_eq(original, "ch1", EQProfile(0, 2, -1, "more lyric presence"))
    farther = experiments.move_microphone(original, "ch1", 20)
    muted = experiments.mute_channel(original, "ch2")
    assert louder.mixer_settings.channels[0].gain == 8
    assert eq.mixer_settings.channels[0].eq.mid == 2
    assert farther.mixer_settings.channels[0].microphone_distance_cm == 32
    assert muted.mixer_settings.channels[1].muted is True
    assert original.mixer_settings.channels[1].muted is False


def test_compare_and_report_are_deterministic():
    setup = piano_and_vocal_setup()
    service = SoundCheckService()
    original = sample_soundcheck()
    changed = SoundCheckExperimentService().change_monitor(original, 2)
    comparison = service.compare(original, changed, setup)
    assert comparison.differences == service.compare(original, changed, setup).differences
    report = service.text_report(service.analyze(original, setup))
    assert "House Mix" in report
    assert "Vocals .......... Balanced" in report


def test_clipping_and_insufficient_gain_are_reported():
    original = sample_soundcheck()
    channels = tuple(
        replace(c, gain=10, fader=8) if c.channel_id == "ch1" else c
        for c in original.mixer_settings.channels
    )
    loud = replace(original, mixer_settings=replace(original.mixer_settings, channels=channels))
    analysis = SoundCheckService().analyze(loud, piano_and_vocal_setup())
    assert analysis.clipping_risk is True
