from open_mic_lab.sample_data import sample_audience_performance, sample_audience_profiles
from open_mic_lab.services.audience_service import (
    AudienceExperimentService,
    AudienceResponseService,
)


def test_audience_profiles_load_deterministically() -> None:
    profiles = sample_audience_profiles()
    assert tuple(profiles) == (
        "first-time-open-mic",
        "supportive-coffeehouse",
        "attentive-listening-room",
        "church-congregation",
        "neighborhood-festival",
        "rehearsal-with-friends",
    )
    assert profiles["church-congregation"].participation_comfort == 7


def test_response_analysis_has_no_score_and_structured_observations() -> None:
    response = AudienceResponseService().analyze(
        sample_audience_performance(), sample_audience_profiles()["supportive-coffeehouse"]
    )
    assert not hasattr(response, "score")
    assert response.strengths
    assert response.explanations
    assert "flowchart LR" in response.mermaid_diagram


def test_adaptation_experiment_is_immutable_and_changes_analysis() -> None:
    performance = sample_audience_performance()
    profile = sample_audience_profiles()["church-congregation"]
    result = AudienceExperimentService().replace_one_unfamiliar_song(performance, profile)
    assert result.changed_performance is not performance
    assert performance.identifier == "chapter-10-sample-set"
    assert result.changed_performance.identifier.endswith("-familiarity")
    assert result.original_response != result.changed_response


def test_comparison_service_reports_profile_differences() -> None:
    profiles = sample_audience_profiles()
    comparison = AudienceResponseService().compare(
        sample_audience_performance(),
        profiles["supportive-coffeehouse"],
        profiles["church-congregation"],
    )
    assert comparison.left_profile == "Supportive coffeehouse audience"
    assert comparison.reflection_prompts
    assert comparison.different_observations
