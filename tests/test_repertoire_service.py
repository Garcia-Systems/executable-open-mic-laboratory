from open_mic_lab.sample_data import build_sample_repertoire
from open_mic_lab.services.repertoire_service import describe_repertoire


def test_sample_data_integrity_and_descriptions() -> None:
    rep = build_sample_repertoire()
    assert len(rep.songs) == 6
    assert len(rep.versions) == 7
    lines = describe_repertoire(rep)
    assert lines[0].startswith("river-guitar-original: River Road at Dusk")
    assert any("piano/vocal" in line for line in lines)
