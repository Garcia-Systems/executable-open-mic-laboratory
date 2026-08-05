from datetime import date

from open_mic_lab.domain import PracticeGoal, PracticeTask, SkillArea
from open_mic_lab.sample_data import (
    build_sample_repertoire,
    sample_coordination_profile,
    sample_practice_sessions,
)
from open_mic_lab.services.practice_service import (
    PracticeAnalyticsService,
    PracticePlanningInput,
    PracticePlanningService,
)


def _plan(minutes=30, goal=PracticeGoal.BALANCED_IMPROVEMENT):
    return PracticePlanningService().generate_plan(
        build_sample_repertoire(),
        sample_practice_sessions(),
        sample_coordination_profile(),
        PracticePlanningInput(
            minutes, date(2026, 8, 5), goal, learner_priorities=(SkillArea.COORDINATION,)
        ),
    )


def test_practice_plan_generation_is_deterministic():
    assert _plan() == _plan()
    assert _plan().estimated_duration_minutes == 30


def test_practice_block_sequencing_and_duration():
    plan = _plan()
    assert plan.blocks[0].task is PracticeTask.WARM_UP
    assert plan.blocks[-1].task in {PracticeTask.REFLECTION, PracticeTask.PERFORMANCE_RUN_THROUGH}
    assert all(block.duration_minutes > 0 for block in plan.blocks)


def test_priorities_include_coordination_and_readiness():
    priorities = PracticePlanningService().priorities(
        build_sample_repertoire(),
        sample_practice_sessions(),
        sample_coordination_profile(),
        PracticePlanningInput(30, date(2026, 8, 5), learner_priorities=(SkillArea.COORDINATION,)),
    )
    assert priorities[0].score >= priorities[-1].score
    assert {item.skill_area for item in priorities} & {SkillArea.COORDINATION, SkillArea.READINESS}


def test_adaptive_experiments_are_immutable():
    service = PracticePlanningService()
    original = _plan()
    changed = service.experiment(original, "performance")
    assert changed is not original
    assert changed.identifier != original.identifier
    assert original.available_minutes == 30
    assert changed.goal is PracticeGoal.PERFORMANCE_PREPARATION


def test_practice_analytics_generate_observations():
    analytics = PracticeAnalyticsService().analyze(_plan(), sample_practice_sessions())
    assert analytics.total_minutes == 30
    assert analytics.distribution
    assert analytics.observations
