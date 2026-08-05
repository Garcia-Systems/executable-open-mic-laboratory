from open_mic_lab.domain import Instrument
from open_mic_lab.sample_data import build_sample_repertoire
from open_mic_lab.services.arrangement_service import (
    ArrangementAnalysisService,
    ArrangementExperimentService,
    ArrangementTimelineService,
)


def test_arrangement_creation_and_repertoire_links_are_deterministic() -> None:
    rep = build_sample_repertoire()
    arrangement = rep.get_arrangement("window-piano-arrangement")
    assert arrangement.source_performance_version_identifier == "window-piano"
    assert arrangement.primary_instrument is Instrument.PIANO_VOCAL
    assert list(rep.arrangements) == list(build_sample_repertoire().arrangements)


def test_immutable_experiments_and_chaining_history() -> None:
    rep = build_sample_repertoire()
    original = rep.get_arrangement("window-piano-arrangement")
    service = ArrangementExperimentService()
    changed = service.combine(
        original,
        lambda item: service.transpose(item, "G", -2),
        service.simplify_accompaniment,
        service.shorten_introduction,
        lambda item: service.alter_tempo(item, 64),
    )
    assert original.performance_key == "A"
    assert changed.performance_key == "G"
    assert changed.target_tempo_bpm == 64
    assert changed.simplification_level == 1
    assert [record.experiment_name for record in changed.history] == [
        "transpose",
        "simplify accompaniment",
        "shorten introduction",
        "alter tempo",
    ]


def test_arrangement_comparison_and_timeline_tradeoffs() -> None:
    rep = build_sample_repertoire()
    service = ArrangementExperimentService()
    original = rep.get_arrangement("window-piano-arrangement")
    guitar = service.switch_primary_instrument(original, Instrument.GUITAR_VOCAL)
    comparison = ArrangementAnalysisService().compare(original, guitar)
    assert any("Instrument" in item for item in comparison.differences)
    assert "not an abstract winner" in comparison.reflection
    timeline = ArrangementTimelineService().timeline(original)
    assert [entry.start_time for entry in timeline[:3]] == ["00:00", "00:20", "00:47"]
    assert sum(entry.duration_seconds for entry in timeline) > 0
