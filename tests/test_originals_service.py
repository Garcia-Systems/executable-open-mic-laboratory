# ruff: noqa: E501

from open_mic_lab.sample_data import (
    build_sample_repertoire,
    sample_original_presentation_plan,
    sample_setlist,
)
from open_mic_lab.services.originals_service import (
    OriginalMusicAnalysisService,
    OriginalPresentationExperimentService,
)


def test_original_music_analysis_reports_without_success_probability():
    rep = build_sample_repertoire()
    plan = sample_original_presentation_plan()
    analysis = OriginalMusicAnalysisService().analyze(plan, sample_setlist(), rep)
    assert "original(s)" in analysis.observations[0]
    assert (
        "success probability"
        not in " ".join(analysis.observations + analysis.educational_explanations).lower()
    )
    assert "Original Song: Window Light" in analysis.mermaid_diagram


def test_placement_experiments_are_immutable():
    plan = sample_original_presentation_plan()
    changed = OriginalPresentationExperimentService().move_original_earlier(plan)
    assert plan.ordered_version_identifiers == (
        "harbor-guitar",
        "window-piano",
        "train-guitar-closer",
    )
    assert changed.ordered_version_identifiers == (
        "window-piano",
        "harbor-guitar",
        "train-guitar-closer",
    )
    assert changed is not plan


def test_story_and_participation_experiments():
    plan = sample_original_presentation_plan()
    service = OriginalPresentationExperimentService()
    shorter = service.shorten_introduction(plan)
    longer = service.lengthen_story(plan)
    participation = service.pair_with_audience_participation(plan)
    assert shorter.introductions[0].duration_seconds < plan.introductions[0].duration_seconds
    assert longer.introductions[0].duration_seconds > plan.introductions[0].duration_seconds
    assert participation.introductions[0].strategy.value == "audience participation"


def test_comparison_service_is_deterministic():
    rep = build_sample_repertoire()
    plan = sample_original_presentation_plan()
    moved = OriginalPresentationExperimentService().move_original_earlier(plan)
    service = OriginalMusicAnalysisService()
    first = service.compare(plan, moved, rep)
    second = service.compare(plan, moved, rep)
    assert first == second
    assert first.reflection_prompts
