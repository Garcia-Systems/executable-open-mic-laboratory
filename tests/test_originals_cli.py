from open_mic_lab.cli import main
from open_mic_lab.debug_labs.chapter_13_original_music import run_debug_lab


def test_originals_analyze_cli(capsys):
    assert main(["originals", "analyze"]) == 0
    output = capsys.readouterr().out
    assert "Observation:" in output
    assert "Explanation:" in output


def test_originals_compare_cli(capsys):
    assert main(["originals", "compare"]) == 0
    output = capsys.readouterr().out
    assert "Compare:" in output
    assert "Reflection:" in output


def test_originals_experiment_cli(capsys):
    assert main(["originals", "experiment", "placement"]) == 0
    output = capsys.readouterr().out
    assert "Original object unchanged: True" in output


def test_originals_identity_cli(capsys):
    assert main(["originals", "identity"]) == 0
    output = capsys.readouterr().out
    assert "reflective tool" in output


def test_chapter_thirteen_demo_cli(capsys):
    assert main(["chapter-thirteen-demo"]) == 0
    output = capsys.readouterr().out
    assert "Chapter 13" in output
    assert "Deferred to Chapter 14" in output


def test_chapter_thirteen_debug_helper():
    result = run_debug_lab()
    assert result["observation_count"] >= 2
    assert result["original_unchanged"] is True
