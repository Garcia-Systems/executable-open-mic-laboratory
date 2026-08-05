from open_mic_lab.cli import main
from open_mic_lab.debug_labs.chapter_05_coordination import run_debug_lab


def test_coordination_cli_commands(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["coordination", "analyze"]) == 0
    assert "Coordination score" in capsys.readouterr().out
    assert main(["coordination", "bottlenecks"]) == 0
    assert "Bottleneck" in capsys.readouterr().out
    assert main(["coordination", "ladder"]) == 0
    assert "60 BPM" in capsys.readouterr().out
    assert main(["coordination", "experiment", "simplify"]) == 0
    assert "Original object unchanged: True" in capsys.readouterr().out
    assert main(["coordination", "experiment", "tempo", "60"]) == 0
    assert "After:" in capsys.readouterr().out
    assert main(["chapter-five-demo"]) == 0
    assert "Automaticity reduces cognitive load" in capsys.readouterr().out


def test_chapter_five_debug_helper() -> None:
    snapshot = run_debug_lab()
    assert snapshot["original_unchanged"] is True
    assert snapshot["ladder"] == (60, 66, 72)
    assert snapshot["simplified_score"] > snapshot["baseline_score"]
