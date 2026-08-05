"""CLI tests for Chapter 14."""

from open_mic_lab.cli import main


def test_event_timeline_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["event", "timeline"]) == 0
    output = capsys.readouterr().out
    assert "18:30 Arrive" in output
    assert "19:45 Reflection" in output


def test_event_report_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["event", "report"]) == 0
    output = capsys.readouterr().out
    assert "Event report: first open mic" in output
    assert "Sound check:" in output
    assert "Original music:" in output


def test_event_experiment_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["event", "experiment", "equipment-change"]) == 0
    output = capsys.readouterr().out
    assert "Original unchanged: True" in output


def test_chapter_fourteen_demo_cli(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main(["chapter-fourteen-demo"]) == 0
    output = capsys.readouterr().out
    assert "Chapter 14" in output
    assert "final event report" in output
