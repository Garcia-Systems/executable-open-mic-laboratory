from open_mic_lab.debug_labs.chapter_04_arrangements import main, run_lab


def test_chapter_04_debug_helper_exposes_meaningful_variables(capsys) -> None:  # type: ignore[no-untyped-def]
    result = run_lab()
    assert result["immutable_original_key"] == "A"
    assert len(result["experiment_history"]) == 4
    assert result["total_timeline_seconds"] == 181
    assert main() == 0
    out = capsys.readouterr().out
    assert "Chapter 4 arrangement debug lab" in out
