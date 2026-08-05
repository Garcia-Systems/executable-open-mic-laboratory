from open_mic_lab.cli import main
from open_mic_lab.debug_labs.chapter_06_practice_engineering import build_debug_practice_plan


def test_practice_cli_commands(capsys):
    assert main(["practice", "plan"]) == 0
    assert "Practice plan" in capsys.readouterr().out
    assert main(["practice", "analyze"]) == 0
    assert "Observation" in capsys.readouterr().out
    assert main(["practice", "priorities"]) == 0
    assert "readiness" in capsys.readouterr().out
    assert main(["practice", "blocks"]) == 0
    assert "warm-up" in capsys.readouterr().out
    assert main(["practice", "experiment", "maintenance"]) == 0
    assert "Original object unchanged: True" in capsys.readouterr().out


def test_chapter_six_demo(capsys):
    assert main(["chapter-six-demo"]) == 0
    assert "Chapter 6" in capsys.readouterr().out


def test_chapter_six_debug_helper(capsys):
    build_debug_practice_plan()
    assert "debug lab" in capsys.readouterr().out
