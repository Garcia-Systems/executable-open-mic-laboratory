from open_mic_lab.debug_labs.chapter_15_performance_analytics import run_debug_lab


def test_chapter_15_debug_lab_exposes_key_variables() -> None:
    data = run_debug_lab()
    assert data["baseline_unchanged"] is True
    assert "dashboard" in data
    assert "recommendations" in data
