from open_mic_lab.debug_labs.chapter_03_building_a_set import run_lab


def test_chapter_03_debug_helper_exposes_meaningful_variables() -> None:
    result = run_lab()
    assert "timeline" in result
    assert result["cumulative_running_time"] == 715
    assert result["immutable_original_order"] != result["experiment_order"]
