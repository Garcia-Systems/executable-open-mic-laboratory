from open_mic_lab.cli import main
from open_mic_lab.debug_labs.chapter_12_improvisation import run_debug_lab


def test_improv_analyze_cli(capsys):
    assert main(["improv", "analyze"]) == 0
    output = capsys.readouterr().out
    assert "Observation:" in output
    assert "Option:" in output


def test_improv_experiment_cli(capsys):
    assert main(["improv", "experiment", "chorus"]) == 0
    output = capsys.readouterr().out
    assert "Planned:" in output
    assert "Original object unchanged: True" in output


def test_chapter_twelve_demo_cli(capsys):
    assert main(["chapter-twelve-demo"]) == 0
    output = capsys.readouterr().out
    assert "Chapter 12" in output
    assert "Reflection:" in output


def test_chapter_twelve_debug_helper():
    result = run_debug_lab()
    assert result["opportunity_count"] >= 4
    assert result["original_unchanged"] is True
