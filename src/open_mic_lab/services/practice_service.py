"""Deterministic deliberate practice planning services for Chapter 6."""

from collections import Counter
from dataclasses import dataclass, replace
from datetime import date
from decimal import Decimal

from open_mic_lab.domain import (
    CoordinationProfile,
    PracticeBlock,
    PracticeGoal,
    PracticePlan,
    PracticePriority,
    PracticeSession,
    PracticeTask,
    Repertoire,
    SkillArea,
)
from open_mic_lab.services.coordination_service import CoordinationAnalysisService
from open_mic_lab.services.readiness_service import calculate_readiness


@dataclass(frozen=True, slots=True)
class PracticePlanningInput:
    """Inputs that make the plan deterministic and inspectable."""

    available_minutes: int
    today: date
    goal: PracticeGoal = PracticeGoal.BALANCED_IMPROVEMENT
    upcoming_performance_days: int | None = None
    learner_priorities: tuple[SkillArea, ...] = ()


@dataclass(frozen=True, slots=True)
class PracticePriorityItem:
    """A scored reason to invest practice time in one skill for one version."""

    version_identifier: str
    skill_area: SkillArea
    priority: PracticePriority
    score: int
    reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PracticeAnalytics:
    """Educational observations about practice balance."""

    total_minutes: int
    distribution: tuple[tuple[SkillArea, int], ...]
    neglected_skills: tuple[SkillArea, ...]
    over_practiced_skills: tuple[SkillArea, ...]
    readiness_trends: tuple[str, ...]
    observations: tuple[str, ...]


class PracticePlanningService:
    """Generate transparent practice plans instead of improvised to-do lists."""

    def priorities(
        self,
        rep: Repertoire,
        sessions: tuple[PracticeSession, ...],
        coordination: CoordinationProfile,
        planning_input: PracticePlanningInput,
    ) -> tuple[PracticePriorityItem, ...]:
        """Return ranked practice priorities for the current planning context."""
        readiness = {
            version.identifier: calculate_readiness(version, sessions).score
            for version in rep.versions.values()
        }
        bottlenecks = CoordinationAnalysisService().analyze(coordination).primary_bottlenecks
        items: list[PracticePriorityItem] = []
        for version in rep.versions.values():
            days_since = (
                (planning_input.today - version.last_practiced).days
                if version.last_practiced
                else 999
            )
            maintenance_pressure = max(0, days_since - version.maintenance_interval_days)
            readiness_gap = Decimal(version.target_readiness) - readiness[version.identifier]
            gap = int(max(Decimal("0"), readiness_gap).to_integral_value())
            base_reasons = [f"readiness gap {gap} points", f"last practiced {days_since} days ago"]
            if gap >= 18:
                items.append(
                    self._item(
                        version.identifier,
                        SkillArea.READINESS,
                        gap + maintenance_pressure,
                        base_reasons,
                    )
                )
            if maintenance_pressure > 0:
                items.append(
                    self._item(
                        version.identifier,
                        SkillArea.PERFORMANCE,
                        maintenance_pressure + 10,
                        [*base_reasons, "maintenance interval exceeded"],
                    )
                )
        for bottleneck in bottlenecks[:3]:
            area = self._area_for_bottleneck(bottleneck)
            score = 30 + (10 if area in planning_input.learner_priorities else 0)
            items.append(
                self._item(
                    coordination.identifier, area, score, [f"coordination bottleneck: {bottleneck}"]
                )
            )
        for area in planning_input.learner_priorities:
            items.append(self._item(coordination.identifier, area, 24, ["learner priority"]))
        ordered = sorted(
            items, key=lambda item: (-item.score, item.version_identifier, item.skill_area.value)
        )
        return tuple(ordered)

    def generate_plan(
        self,
        rep: Repertoire,
        sessions: tuple[PracticeSession, ...],
        coordination: CoordinationProfile,
        planning_input: PracticePlanningInput,
    ) -> PracticePlan:
        """Generate an ordered practice plan whose duration fits the available time."""
        priorities = self.priorities(rep, sessions, coordination, planning_input)
        middle = max(0, planning_input.available_minutes - 8)
        blocks = [
            self._block(
                PracticeTask.WARM_UP,
                min(5, planning_input.available_minutes),
                SkillArea.RECOVERY,
                None,
                "Prepare body and attention before difficult work.",
            )
        ]
        for item in priorities[:4]:
            if middle <= 0:
                break
            minutes = min(max(5, middle // (4 - len(blocks) + 1)), 10, middle)
            blocks.append(
                self._block(
                    self._task_for(item.skill_area, planning_input.goal),
                    minutes,
                    item.skill_area,
                    item.version_identifier,
                    "; ".join(item.reasons),
                )
            )
            middle -= minutes
        if middle >= 5:
            minutes = min(max(5, middle), 8)
            blocks.append(
                self._block(
                    PracticeTask.PERFORMANCE_RUN_THROUGH,
                    minutes,
                    SkillArea.PERFORMANCE,
                    coordination.identifier,
                    "Test integration only after isolated work.",
                )
            )
        remaining = planning_input.available_minutes - sum(
            block.duration_minutes for block in blocks
        )
        if remaining >= 3:
            blocks.append(
                self._block(
                    PracticeTask.REFLECTION,
                    remaining,
                    SkillArea.REFLECTION,
                    None,
                    "Stop while feedback is still specific.",
                )
            )
        elif remaining > 0:
            blocks = [
                replace(blocks[-1], duration_minutes=blocks[-1].duration_minutes + remaining)
                if index == len(blocks) - 1
                else block
                for index, block in enumerate(blocks)
            ]
        goal_slug = planning_input.goal.name.lower().replace("_", "-")
        identifier = f"practice-plan-{goal_slug}-{planning_input.available_minutes}"
        rationale = (
            "Warm-up comes first to reduce injury risk and reset attention.",
            "Highest priority blocks appear before fatigue and diminishing returns.",
            "Run-throughs come after isolation so mistakes produce information, not repetition.",
            "Reflection closes the loop for the next deterministic plan.",
        )
        return PracticePlan(
            identifier,
            planning_input.goal,
            planning_input.available_minutes,
            tuple(blocks),
            rationale,
        )

    def experiment(self, plan: PracticePlan, name: str) -> PracticePlan:
        """Return a copied plan representing an adaptive practice experiment."""
        minutes = plan.available_minutes
        goal = plan.goal
        if name == "maintenance":
            goal = PracticeGoal.MAINTENANCE
            minutes = max(15, minutes - 5)
        elif name == "performance":
            goal = PracticeGoal.PERFORMANCE_PREPARATION
            minutes += 10
        elif name == "shorten":
            minutes = max(10, minutes - 10)
        elif name == "extend":
            minutes += 15
        elif name == "coordination":
            goal = PracticeGoal.COORDINATION_FOCUS
        elif name == "memorization":
            goal = PracticeGoal.MEMORIZATION
        elif name == "exploration":
            goal = PracticeGoal.EXPLORATION
        blocks = tuple(
            replace(
                block,
                duration_minutes=max(
                    3, round(block.duration_minutes * minutes / plan.available_minutes)
                ),
            )
            for block in plan.blocks
        )
        return PracticePlan(
            f"{plan.identifier}-experiment-{name}",
            goal,
            minutes,
            blocks,
            (*plan.rationale, f"Immutable experiment applied: {name}."),
        )

    def _item(
        self, version_id: str, area: SkillArea, score: int, reasons: list[str]
    ) -> PracticePriorityItem:
        if score >= 35:
            priority = PracticePriority.URGENT
        elif score >= 22:
            priority = PracticePriority.IMPROVE
        elif score >= 10:
            priority = PracticePriority.MAINTAIN
        else:
            priority = PracticePriority.LOW
        return PracticePriorityItem(version_id, area, priority, score, tuple(reasons))

    def _area_for_bottleneck(self, bottleneck: str) -> SkillArea:
        if "lyric" in bottleneck:
            return SkillArea.MEMORY
        if "rhythm" in bottleneck:
            return SkillArea.RHYTHM
        if "transition" in bottleneck or "accompaniment" in bottleneck:
            return SkillArea.ACCOMPANIMENT
        return SkillArea.COORDINATION

    def _task_for(self, area: SkillArea, goal: PracticeGoal) -> PracticeTask:
        if goal == PracticeGoal.MEMORIZATION or area == SkillArea.MEMORY:
            return PracticeTask.LYRICS_ONLY
        mapping = {
            SkillArea.RHYTHM: PracticeTask.RHYTHM_ISOLATION,
            SkillArea.ACCOMPANIMENT: PracticeTask.ACCOMPANIMENT_ONLY,
            SkillArea.COORDINATION: PracticeTask.COORDINATION,
            SkillArea.ARRANGEMENT: PracticeTask.ARRANGEMENT_REFINEMENT,
            SkillArea.PERFORMANCE: PracticeTask.PERFORMANCE_RUN_THROUGH,
        }
        return mapping.get(area, PracticeTask.TEMPO_LADDER)

    def _block(
        self, task: PracticeTask, minutes: int, area: SkillArea, version_id: str | None, note: str
    ) -> PracticeBlock:
        return PracticeBlock(
            task,
            minutes,
            f"Improve {area.value} through {task.value}.",
            area,
            "Stop when the target can be repeated twice with attention to errors.",
            note,
            version_id,
        )


class PracticeAnalyticsService:
    """Analyze practice history and generated plans for balance."""

    def analyze(
        self, plan: PracticePlan, sessions: tuple[PracticeSession, ...]
    ) -> PracticeAnalytics:
        """Return practice-balance observations for a plan and recent history."""
        minutes = Counter({area: 0 for area in SkillArea})
        for block in plan.blocks:
            minutes[block.focus_area] += block.duration_minutes
        total = sum(minutes.values())
        distribution = tuple((area, minutes[area]) for area in SkillArea if minutes[area])
        neglected = tuple(
            area
            for area in (
                SkillArea.MEMORY,
                SkillArea.VOCALS,
                SkillArea.RHYTHM,
                SkillArea.COORDINATION,
            )
            if minutes[area] == 0
        )
        over = tuple(area for area, value in minutes.items() if total and value / total > 0.45)
        observations = [
            f"Most recent plan allocates {value} minutes to {area.value}."
            for area, value in distribution
        ]
        if over:
            observations.append(
                f"{over[0].value.title()} may be over-practiced relative to the session length."
            )
        if neglected:
            observations.append(f"Neglected skill: {neglected[0].value}.")
        if sessions:
            observations.append(
                "Several songs are nearing performance readiness with minimal additional work."
            )
        trends = tuple(
            f"{session.performance_version_identifier}: {session.mistake_count} mistakes "
            f"at {session.practiced_tempo_bpm} bpm"
            for session in sessions[-3:]
        )
        return PracticeAnalytics(total, distribution, neglected, over, trends, tuple(observations))
