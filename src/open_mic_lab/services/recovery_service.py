"""Deterministic recovery-analysis services for Chapter 11."""

from dataclasses import dataclass, replace

from open_mic_lab.domain.recovery import (
    INCIDENT_CATALOG,
    IncidentReport,
    IncidentType,
    PerformanceIncident,
    RecoveryAction,
    RecoveryOutcome,
    RecoveryStage,
    RecoveryStrategy,
    RecoveryTimeline,
    RecoveryTimelineEvent,
)


@dataclass(frozen=True, slots=True)
class RecoveryScenario:
    """Immutable recovery scenario for analysis and experiments."""

    incident: PerformanceIncident
    context: str
    performer_preparation: str
    communication_plan: str
    preferred_strategy: RecoveryStrategy
    experiment_history: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class RecoveryComparison:
    """Side-by-side educational strategy comparison."""

    left_strategy: RecoveryStrategy
    right_strategy: RecoveryStrategy
    shared_observations: tuple[str, ...]
    different_tradeoffs: tuple[str, ...]
    reflection_prompts: tuple[str, ...]


class IncidentCatalogService:
    """Return deterministic educational incidents."""

    def list_incidents(self) -> tuple[PerformanceIncident, ...]:
        """List catalog incidents in stable order."""
        return INCIDENT_CATALOG

    def get(self, identifier: str) -> PerformanceIncident:
        """Return an incident by identifier."""
        for incident in INCIDENT_CATALOG:
            if incident.identifier == identifier:
                return incident
        raise KeyError(f"Unknown incident '{identifier}'.")


class RecoveryAnalysisService:
    """Analyze recovery options without scoring mistakes or performers."""

    def analyze(self, scenario: RecoveryScenario) -> IncidentReport:
        """Return a deterministic incident report."""
        outcomes = tuple(self._outcome(s) for s in self._likely_strategies(scenario.incident))
        observations = self._observations(scenario.incident, scenario.preferred_strategy)
        strengths = self._strengths(scenario)
        actions = tuple(
            RecoveryAction(
                outcome.strategy, self._action_text(outcome.strategy), outcome.educational_response
            )
            for outcome in outcomes[:4]
        )
        return IncidentReport(
            scenario.incident,
            scenario.context,
            scenario.performer_preparation,
            scenario.communication_plan,
            observations,
            strengths,
            self.timeline(scenario),
            actions,
            (
                "What did the audience likely experience: the incident, the recovery, or both?",
                "Which recovery choice preserved the musical story most clearly?",
                "What preparation would make this decision easier next time?",
            ),
            outcomes,
        )

    def timeline(self, scenario: RecoveryScenario) -> RecoveryTimeline:
        """Generate a deterministic recovery timeline."""
        delay = 2 if scenario.preferred_strategy is RecoveryStrategy.CONTINUE_IMMEDIATELY else 5
        if scenario.incident.technical:
            delay += 3
        events = (
            RecoveryTimelineEvent(
                RecoveryStage.MISTAKE_OCCURS,
                scenario.incident.incident_type.value,
                0,
                scenario.incident.description,
            ),
            RecoveryTimelineEvent(
                RecoveryStage.PERFORMER_RECOGNIZES,
                "Recognition",
                1,
                "The performer notices a change and keeps listening.",
            ),
            RecoveryTimelineEvent(
                RecoveryStage.RECOVERY_DECISION,
                scenario.preferred_strategy.value,
                delay,
                self._action_text(scenario.preferred_strategy),
            ),
            RecoveryTimelineEvent(
                RecoveryStage.AUDIENCE_PERCEPTION,
                "Audience perception",
                delay + 2,
                "Listeners receive the continuity choice more than a private self-judgment.",
            ),
            RecoveryTimelineEvent(
                RecoveryStage.PERFORMANCE_CONTINUES,
                "Performance continues",
                delay + 6,
                "The song or set returns to a shared musical path.",
            ),
            RecoveryTimelineEvent(
                RecoveryStage.REFLECTION,
                "Reflection",
                delay + 60,
                "Afterward, the learner turns the event into preparation data.",
            ),
        )
        return RecoveryTimeline(scenario.incident.identifier, scenario.preferred_strategy, events)

    def compare(self, left: RecoveryScenario, right: RecoveryScenario) -> RecoveryComparison:
        """Compare two recovery strategies as educational tradeoffs."""
        left_report = self.analyze(left)
        right_report = self.analyze(right)
        shared = tuple(o for o in left_report.observations if o in right_report.observations)
        different = tuple(
            dict.fromkeys(
                [f"{left.preferred_strategy.value}: {o}" for o in left_report.observations]
                + [f"{right.preferred_strategy.value}: {o}" for o in right_report.observations]
            )
        )
        return RecoveryComparison(
            left.preferred_strategy,
            right.preferred_strategy,
            shared,
            different,
            ("Which strategy best protects flow?", "Which strategy best protects clarity?"),
        )

    def _likely_strategies(self, incident: PerformanceIncident) -> tuple[RecoveryStrategy, ...]:
        if incident.incident_type in {
            IncidentType.MICROPHONE_FAILURE,
            IncidentType.CABLE_DISCONNECTED,
            IncidentType.BROKEN_STRING,
            IncidentType.MONITOR_PROBLEM,
        }:
            return (
                RecoveryStrategy.STOP_AND_EXPLAIN,
                RecoveryStrategy.INSTRUMENTAL_RECOVERY,
                RecoveryStrategy.SIMPLIFY_ACCOMPANIMENT,
                RecoveryStrategy.CONTINUE_IMMEDIATELY,
            )
        if incident.incident_type is IncidentType.TEMPO_DRIFT:
            return (
                RecoveryStrategy.TEMPO_RESET,
                RecoveryStrategy.SIMPLIFY_ACCOMPANIMENT,
                RecoveryStrategy.CONTINUE_IMMEDIATELY,
            )
        if incident.incident_type is IncidentType.FORGOTTEN_LYRICS:
            return (
                RecoveryStrategy.CONTINUE_IMMEDIATELY,
                RecoveryStrategy.INVITE_AUDIENCE_PARTICIPATION,
                RecoveryStrategy.INSTRUMENTAL_RECOVERY,
                RecoveryStrategy.RESTART_SECTION,
            )
        return (
            RecoveryStrategy.CONTINUE_IMMEDIATELY,
            RecoveryStrategy.RESTART_SECTION,
            RecoveryStrategy.SIMPLIFY_ACCOMPANIMENT,
            RecoveryStrategy.SKIP_VERSE,
        )

    def _observations(
        self, incident: PerformanceIncident, strategy: RecoveryStrategy
    ) -> tuple[str, ...]:
        base = ["Incidents are modeled as educational scenarios rather than predictions."]
        if strategy is RecoveryStrategy.CONTINUE_IMMEDIATELY:
            base.append("Continuing confidently may preserve performance flow.")
        if strategy is RecoveryStrategy.RESTART_SECTION:
            base.append("Restarting may improve musical accuracy but interrupt pacing.")
        if strategy is RecoveryStrategy.SIMPLIFY_ACCOMPANIMENT:
            base.append("Simplifying accompaniment reduces coordination demands.")
        if strategy is RecoveryStrategy.INVITE_AUDIENCE_PARTICIPATION:
            base.append("Audience participation can create a natural recovery opportunity.")
        if incident.technical:
            base.append(
                "Technical incidents may require clear communication and signal-path attention."
            )
        if incident.audience_noticeability <= 4:
            base.append("The performer may notice more detail than the audience receives.")
        return tuple(base)

    def _strengths(self, scenario: RecoveryScenario) -> tuple[str, ...]:
        strengths = ["A named recovery strategy turns surprise into a decision."]
        if (
            "cue" in scenario.communication_plan.lower()
            or "thank" in scenario.communication_plan.lower()
        ):
            strengths.append("The communication plan includes audience-facing language.")
        if (
            "practice" in scenario.performer_preparation.lower()
            or "rehears" in scenario.performer_preparation.lower()
        ):
            strengths.append("Preparation evidence can reduce recovery decision time.")
        return tuple(strengths)

    def _outcome(self, strategy: RecoveryStrategy) -> RecoveryOutcome:
        table = {
            RecoveryStrategy.CONTINUE_IMMEDIATELY: (
                "flow preserved",
                "The audience may experience confidence more than the detail.",
                (),
                "Keep time, breathe, and rejoin the next reliable cue.",
            ),
            RecoveryStrategy.RESTART_SECTION: (
                "flow interrupted",
                "Accuracy can improve while pacing becomes more explicit.",
                (),
                "Name the restart briefly and return with steady tempo.",
            ),
            RecoveryStrategy.SIMPLIFY_ACCOMPANIMENT: (
                "flow supported",
                "Texture may thin while coordination improves.",
                (),
                "Reduce accompaniment load until the form is secure.",
            ),
            RecoveryStrategy.INVITE_AUDIENCE_PARTICIPATION: (
                "flow redirected",
                "A shared refrain can turn recovery into connection.",
                (),
                "Use only low-pressure invitations.",
            ),
            RecoveryStrategy.SKIP_VERSE: (
                "form shortened",
                "Most listeners may follow the musical continuity.",
                (),
                "Move to the next known section deliberately.",
            ),
            RecoveryStrategy.STOP_AND_EXPLAIN: (
                "flow paused",
                "Clear explanation can reduce confusion.",
                ("Check signal path before resuming.",),
                "Use concise, calm language.",
            ),
            RecoveryStrategy.INSTRUMENTAL_RECOVERY: (
                "flow bridged",
                "Instrumental space can hide navigation work.",
                (),
                "Loop a stable progression and find the next vocal cue.",
            ),
            RecoveryStrategy.TEMPO_RESET: (
                "pulse clarified",
                "A visible breath or count-in can restore ensemble timing.",
                (),
                "Reset pulse at a phrase boundary.",
            ),
        }
        continuity, impact, tech, response = table[strategy]
        return RecoveryOutcome(strategy, continuity, impact, tech, response)

    def _action_text(self, strategy: RecoveryStrategy) -> str:
        return self._outcome(strategy).educational_response


class RecoveryExperimentService:
    """Create immutable recovery experiments."""

    def with_strategy(
        self, scenario: RecoveryScenario, strategy: RecoveryStrategy
    ) -> RecoveryScenario:
        """Return a new scenario with a different recovery strategy."""
        return replace(
            scenario,
            preferred_strategy=strategy,
            experiment_history=scenario.experiment_history + (f"strategy: {strategy.value}",),
        )
