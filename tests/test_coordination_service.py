from open_mic_lab.domain import CoordinationExperiment
from open_mic_lab.sample_data import sample_coordination_profile
from open_mic_lab.services.coordination_service import (
    CoordinationAnalysisService,
    CoordinationExperimentService,
    TempoLadderService,
)


def test_coordination_scoring_is_deterministic() -> None:
    profile = sample_coordination_profile()
    service = CoordinationAnalysisService()
    first = service.analyze(profile)
    second = service.analyze(profile)
    assert first == second
    assert first.coordination_score == 39
    assert first.cognitive_load.score == 61
    assert "Educational model only" in first.model_note


def test_bottlenecks_and_focus_are_educational() -> None:
    result = CoordinationAnalysisService().analyze(sample_coordination_profile())
    assert result.primary_bottlenecks[:3] == (
        "accompaniment complexity",
        "breathing",
        "left-hand independence",
    )
    assert "simplify accompaniment" in result.suggested_practice_focus[0]


def test_tempo_ladder_generation() -> None:
    ladder = TempoLadderService().generate(60, 90, 6)
    assert ladder.tempos == (60, 66, 72, 78, 84, 90)
    assert "Gradual tempo" in ladder.explanation


def test_coordination_experiments_are_immutable_and_improve_analysis() -> None:
    profile = sample_coordination_profile()
    original = CoordinationExperiment(profile)
    service = CoordinationExperimentService()
    analyzer = CoordinationAnalysisService()
    simplified = service.simplify_accompaniment(original)
    lyrics = service.practice_lyrics_only(original)
    accompaniment = service.practice_accompaniment_only(original)
    combined = service.combine_voice_and_accompaniment(original)
    rhythm = service.isolate_rhythm(original)
    faster = service.increase_tempo_gradually(original, 78)

    assert original.profile.identifier == "window-piano-coordination"
    assert simplified.profile.identifier.endswith("-simplified")
    assert simplified.history[0].source_profile_identifier == original.profile.identifier
    assert (
        analyzer.analyze(simplified.profile).coordination_score
        > analyzer.analyze(profile).coordination_score
    )
    assert lyrics.profile.vocal_task.lyric_familiarity == 8
    assert accompaniment.profile.accompaniment_task.rhythm_consistency == 8
    assert combined.profile.hand_voice_independence == 6
    assert rhythm.profile.accompaniment_task.rhythm_consistency == 9
    assert faster.profile.recent_practice_minutes == 60
