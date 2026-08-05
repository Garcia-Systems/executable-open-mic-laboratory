from open_mic_lab.debug_labs.chapter_11_recovery import build_debug_recovery_story


def test_chapter_11_debug_helper_returns_story() -> None:
    story = build_debug_recovery_story()
    assert "timeline" in story
    assert story["original_strategy"].value == "continue immediately"  # type: ignore[union-attr]
