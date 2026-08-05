from open_mic_lab.debug_labs.chapter_10_audience_experience import run_lab


def test_chapter_10_debug_lab_returns_inspectable_values() -> None:
    values = run_lab()
    assert values["original_unchanged"] is True
    assert values["changed_is_copy"] is True
    assert "coffeehouse_response" in values
