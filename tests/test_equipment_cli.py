"""CLI tests for Chapter 8 equipment commands."""

from open_mic_lab.cli import main


def test_equipment_templates_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["equipment", "templates"]) == 0
    assert "piano-and-vocal" in capsys.readouterr().out


def test_equipment_visualize_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["equipment", "visualize"]) == 0
    assert "Main Speakers" in capsys.readouterr().out


def test_chapter_eight_demo_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["chapter-eight-demo"]) == 0
    out = capsys.readouterr().out
    assert "disconnect one cable" in out
    assert "Reflection" in out
