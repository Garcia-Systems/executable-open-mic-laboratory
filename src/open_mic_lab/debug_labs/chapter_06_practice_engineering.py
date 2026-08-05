"""Debug laboratory for Chapter 6 deliberate practice engineering."""

from datetime import date

from open_mic_lab.domain import PracticeGoal, SkillArea
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


def build_debug_practice_plan() -> None:
    """Create variables worth inspecting in a debugger."""
    repertoire = build_sample_repertoire()
    practice_history = sample_practice_sessions()
    coordination_profile = sample_coordination_profile()
    planner = PracticePlanningService()
    planning_input = PracticePlanningInput(
        30,
        date(2026, 8, 5),
        learner_priorities=(SkillArea.COORDINATION,),
    )

    priorities = planner.priorities(  # BREAKPOINT: inspect priority calculation
        repertoire, practice_history, coordination_profile, planning_input
    )
    practice_plan = planner.generate_plan(  # BREAKPOINT: inspect block sequencing
        repertoire, practice_history, coordination_profile, planning_input
    )
    maintenance_plan = planner.experiment(  # BREAKPOINT: inspect immutable experiment
        practice_plan, "maintenance"
    )
    performance_plan = planner.experiment(practice_plan, "performance")
    analytics = PracticeAnalyticsService().analyze(  # BREAKPOINT: inspect observations
        performance_plan, practice_history
    )

    print("Chapter 6 practice engineering debug lab")
    print(f"Priorities: {len(priorities)}")
    print(f"Plan duration: {practice_plan.estimated_duration_minutes} minutes")
    print(f"Maintenance plan: {maintenance_plan.estimated_duration_minutes} minutes")
    print(f"Performance plan: {performance_plan.estimated_duration_minutes} minutes")
    for observation in analytics.observations:
        print(f"Observation: {observation}")
    print(f"Goal example: {PracticeGoal.BALANCED_IMPROVEMENT.value}")


if __name__ == "__main__":
    build_debug_practice_plan()
