"""Tests for Chapter 14 debug lab."""

from open_mic_lab.debug_labs.chapter_14_open_mic import main, run_debug_lab


def test_debug_lab_returns_inspectable_state() -> None:
    result = run_debug_lab()

    assert "event" in result
    assert "report" in result
    assert result["original_unchanged"] is True


def test_debug_lab_main(capsys) -> None:  # type: ignore[no-untyped-def]
    assert main() == 0
    assert "Chapter 14 debug lab" in capsys.readouterr().out
