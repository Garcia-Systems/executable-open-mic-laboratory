from open_mic_lab.domain import SetList
from open_mic_lab.sample_data import build_sample_repertoire, sample_setlist, sample_venue
from open_mic_lab.services.setlist_service import analyze_setlist, estimated_duration_minutes


def test_duration_and_validation_fit() -> None:
    rep = build_sample_repertoire()
    analysis = analyze_setlist(sample_setlist(), rep, sample_venue())
    assert estimated_duration_minutes(sample_setlist(), rep) == 11
    assert analysis.fits_venue is True
    assert analysis.tempo_summary == "min 72 bpm, max 148 bpm"


def test_warnings_for_lack_of_contrast_and_closer() -> None:
    rep = build_sample_repertoire()
    flat = SetList(
        "flat", "Flat", ("river-guitar-lowered", "river-guitar-original"), 15, "corner-cafe"
    )
    warnings = analyze_setlist(flat, rep, sample_venue()).warnings
    assert any("one genre" in warning for warning in warnings)
    assert any("one mood" in warning for warning in warnings)
    assert any("strongest available closer" in warning for warning in warnings)
