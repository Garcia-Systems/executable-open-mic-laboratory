from open_mic_lab.debug_labs.chapter_09_sound_check import run_lab


def test_chapter_09_debug_lab_returns_expected_variables():
    result = run_lab()
    assert result["venue"].identifier == "noisy-cafe"
    assert len(result["workflow"]) == 7
    assert result["immutable_original_monitor"] == 3
    assert result["raised_monitor"].mixer_settings.monitor_mix.overall_level == 5
    assert result["comparison"].differences
