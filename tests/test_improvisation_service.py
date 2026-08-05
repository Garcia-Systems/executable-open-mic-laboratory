from open_mic_lab.domain import (
    ImprovisationConstraint,
    ImprovisationDecision,
    ImprovisationOpportunity,
)
from open_mic_lab.sample_data import (
    build_sample_repertoire,
    sample_audience_profiles,
    sample_improvisation_context,
)
from open_mic_lab.services.improvisation_service import (
    ImprovisationAnalysisService,
    ImprovisationExperimentService,
)


def _fixture():
    rep = build_sample_repertoire()
    context = sample_improvisation_context()
    arrangement = rep.get_arrangement(context.arrangement_identifier)
    audience = sample_audience_profiles()[context.audience_profile_identifier]
    return context, arrangement, audience


def test_detects_deterministic_opportunities_and_constraints():
    context, arrangement, audience = _fixture()
    report = ImprovisationAnalysisService().analyze(context, arrangement, audience)
    opportunities = {option.opportunity for option in report.options}
    assert ImprovisationOpportunity.REPEAT_CHORUS in opportunities
    assert ImprovisationOpportunity.EXTEND_ENDING in opportunities
    assert any(
        ImprovisationConstraint.REMAINING_TIME in option.constraints for option in report.options
    )
    assert report == ImprovisationAnalysisService().analyze(context, arrangement, audience)


def test_immutable_experiments_create_adaptive_timelines():
    _, arrangement, _ = _fixture()
    analyzer = ImprovisationAnalysisService()
    planned = analyzer.planned_timeline(arrangement)
    changed = ImprovisationExperimentService().experiment(
        planned, ImprovisationDecision.REPEAT_CHORUS
    )
    assert planned is not changed
    assert planned.decisions == ()
    assert changed.decisions == (ImprovisationDecision.REPEAT_CHORUS,)
    assert changed.total_duration_seconds == planned.total_duration_seconds + 35
    assert [s.label for s in changed.sections].count("Chorus") > [
        s.label for s in planned.sections
    ].count("Chorus")


def test_timeline_comparison_explains_changes():
    _, arrangement, _ = _fixture()
    analyzer = ImprovisationAnalysisService()
    experiments = ImprovisationExperimentService()
    planned = analyzer.planned_timeline(arrangement)
    adapted = experiments.experiment(planned, ImprovisationDecision.ADD_AUDIENCE_PARTICIPATION)
    comparison = analyzer.compare(planned, adapted)
    assert comparison.planned == planned
    assert comparison.adapted == adapted
    assert any("Audience Participation" in difference for difference in comparison.differences)
