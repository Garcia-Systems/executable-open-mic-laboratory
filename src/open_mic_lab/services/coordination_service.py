"""Chapter 5 deterministic coordination model."""

# Evidence basis for scoring and recommendation services.
#
# Purpose: provide deterministic educational comparisons for repertoire,
# practice, stagecraft, audio workflow, audience scenarios, recovery,
# improvisation, and reflection.
# Inputs: typed domain objects and bounded scenario data in the repository.
# Outputs: scores, categories, warnings, recommendations, and explanation text.
# Evidence Basis: music education, performance psychology, feedback research,
# self-regulated learning, cognitive-load theory, live-sound practice, and
# simulation-based learning motivate the concepts represented here.
# Repository Contribution: exact weights, thresholds, and formula structures are
# original educational heuristics designed for transparent experimentation.
# Limitations: outputs are non-predictive learning aids. They are not validated
# measurements of artistic worth, audience response, technical safety, or future
# performance success.


# ruff: noqa: D102

from dataclasses import dataclass, replace

from open_mic_lab.domain import (
    CognitiveLoad,
    CoordinationExperiment,
    CoordinationExperimentRecord,
    CoordinationProfile,
)


@dataclass(frozen=True, slots=True)
class CoordinationAnalysis:
    """Result of an educational coordination analysis."""

    profile_identifier: str
    coordination_score: int
    cognitive_load: CognitiveLoad
    primary_bottlenecks: tuple[str, ...]
    suggested_practice_focus: tuple[str, ...]
    contributing_factors: tuple[str, ...]
    model_note: str = (
        "Educational model only: this estimates practice attention demands, "
        "not neurological ability."
    )


@dataclass(frozen=True, slots=True)
class TempoLadder:
    """A gradual, deterministic path from a practice tempo to a performance tempo."""

    start_bpm: int
    target_bpm: int
    step_bpm: int
    tempos: tuple[int, ...]
    explanation: str


class CoordinationAnalysisService:
    """Analyze how singing and accompaniment compete for limited attention."""

    def analyze(self, profile: CoordinationProfile) -> CoordinationAnalysis:
        load = self._load(profile)
        score = max(0, min(100, 100 - load.score))
        bottlenecks = self.bottlenecks(profile)
        return CoordinationAnalysis(
            profile.identifier,
            score,
            load,
            bottlenecks,
            tuple(self._focus_for(item) for item in bottlenecks[:3]),
            self._factors(profile),
        )

    def bottlenecks(self, profile: CoordinationProfile) -> tuple[str, ...]:
        candidates: list[tuple[int, str]] = [
            (10 - profile.hand_voice_independence, "left-hand independence"),
            (10 - profile.vocal_task.lyric_familiarity, "lyric memory"),
            (10 - profile.accompaniment_task.chord_transition_security, "chord transitions"),
            (10 - profile.accompaniment_task.rhythm_consistency, "rhythm consistency"),
            (profile.vocal_task.breathing_complexity, "breathing"),
            (profile.accompaniment_task.arrangement_complexity, "accompaniment complexity"),
        ]
        ordered = sorted(candidates, key=lambda item: (-item[0], item[1]))
        return tuple(name for severity, name in ordered if severity >= 4) or (
            "integration practice",
        )

    def _load(self, profile: CoordinationProfile) -> CognitiveLoad:
        tempo_pressure = max(0, round((profile.tempo_bpm - 60) / 4))
        target_pressure = max(0, round((profile.tempo_bpm - profile.target_tempo_bpm) / 2))
        practice_relief = min(12, profile.recent_practice_minutes // 20)
        automatic_relief = round(
            (
                profile.automaticity.accompaniment
                + profile.automaticity.lyrics
                + profile.automaticity.coordination
            )
            * 1.7
        )
        demand = (
            profile.accompaniment_task.accompaniment_difficulty * 5
            + profile.accompaniment_task.arrangement_complexity * 4
            + (10 - profile.accompaniment_task.chord_transition_security) * 4
            + (10 - profile.accompaniment_task.rhythm_consistency) * 4
            + (10 - profile.vocal_task.lyric_familiarity) * 5
            + (10 - profile.vocal_task.vocal_confidence) * 4
            + profile.vocal_task.breathing_complexity * 3
            + (10 - profile.hand_voice_independence) * 6
            + tempo_pressure
            + target_pressure
            - practice_relief
            - automatic_relief
        )
        score = max(0, min(100, round(demand / 3)))
        if score < 34:
            category = "low"
        elif score < 67:
            category = "moderate"
        else:
            category = "high"
        return CognitiveLoad(
            score,
            category,
            "As accompaniment, lyrics, and coordination become automatic, they demand less "
            "conscious attention.",
        )

    def _factors(self, profile: CoordinationProfile) -> tuple[str, ...]:
        return (
            f"Accompaniment difficulty {profile.accompaniment_task.accompaniment_difficulty}/10.",
            f"Lyric familiarity {profile.vocal_task.lyric_familiarity}/10.",
            f"Vocal confidence {profile.vocal_task.vocal_confidence}/10.",
            f"Tempo {profile.tempo_bpm} bpm against target {profile.target_tempo_bpm} bpm.",
            f"Hand/voice independence {profile.hand_voice_independence}/10.",
            f"Recent practice {profile.recent_practice_minutes} minutes.",
            f"Arrangement complexity {profile.accompaniment_task.arrangement_complexity}/10.",
        )

    def _focus_for(self, bottleneck: str) -> str:
        mapping = {
            "left-hand independence": "alternate spoken lyrics with the left-hand pattern",
            "lyric memory": "practice lyrics only until recall is automatic",
            "chord transitions": "loop the two slowest transitions without singing",
            "rhythm consistency": "isolate rhythm with muted strings or blocked chords",
            "breathing": "mark breath points before combining tasks",
            "accompaniment complexity": "simplify accompaniment before restoring texture",
            "integration practice": "combine voice and accompaniment at a reduced tempo",
        }
        return mapping[bottleneck]


class CoordinationExperimentService:
    """Create immutable practice experiments for coordination profiles."""

    def simplify_accompaniment(self, exp: CoordinationExperiment) -> CoordinationExperiment:
        task = exp.profile.accompaniment_task
        return self._copy(
            exp,
            "simplify accompaniment",
            "simplified",
            "Reduced accompaniment demand so attention can move toward singing.",
            accompaniment_task=replace(
                task,
                accompaniment_difficulty=max(0, task.accompaniment_difficulty - 3),
                arrangement_complexity=max(0, task.arrangement_complexity - 3),
            ),
            automaticity=replace(
                exp.profile.automaticity,
                accompaniment=min(10, exp.profile.automaticity.accompaniment + 2),
            ),
        )

    def reduce_tempo(self, exp: CoordinationExperiment, bpm: int) -> CoordinationExperiment:
        return self._copy(
            exp, "reduce tempo", f"tempo-{bpm}", f"Reduced tempo to {bpm} bpm.", tempo_bpm=bpm
        )

    def practice_lyrics_only(self, exp: CoordinationExperiment) -> CoordinationExperiment:
        vocal = exp.profile.vocal_task
        return self._copy(
            exp,
            "practice lyrics only",
            "lyrics",
            "Improved lyric recall.",
            vocal_task=replace(vocal, lyric_familiarity=min(10, vocal.lyric_familiarity + 3)),
            automaticity=replace(
                exp.profile.automaticity, lyrics=min(10, exp.profile.automaticity.lyrics + 2)
            ),
        )

    def practice_accompaniment_only(self, exp: CoordinationExperiment) -> CoordinationExperiment:
        task = exp.profile.accompaniment_task
        return self._copy(
            exp,
            "practice accompaniment only",
            "accompaniment",
            "Stabilized accompaniment patterns.",
            accompaniment_task=replace(
                task,
                chord_transition_security=min(10, task.chord_transition_security + 2),
                rhythm_consistency=min(10, task.rhythm_consistency + 2),
            ),
            automaticity=replace(
                exp.profile.automaticity,
                accompaniment=min(10, exp.profile.automaticity.accompaniment + 2),
            ),
        )

    def combine_voice_and_accompaniment(
        self, exp: CoordinationExperiment
    ) -> CoordinationExperiment:
        return self._copy(
            exp,
            "combine voice and accompaniment",
            "combined",
            "Practiced the attention handoff between tasks.",
            hand_voice_independence=min(10, exp.profile.hand_voice_independence + 2),
            automaticity=replace(
                exp.profile.automaticity,
                coordination=min(10, exp.profile.automaticity.coordination + 2),
            ),
        )

    def increase_tempo_gradually(
        self, exp: CoordinationExperiment, bpm: int
    ) -> CoordinationExperiment:
        return self._copy(
            exp,
            "increase tempo gradually",
            f"tempo-{bpm}",
            f"Raised tempo gradually to {bpm} bpm.",
            tempo_bpm=bpm,
            recent_practice_minutes=exp.profile.recent_practice_minutes + 20,
        )

    def isolate_rhythm(self, exp: CoordinationExperiment) -> CoordinationExperiment:
        task = exp.profile.accompaniment_task
        return self._copy(
            exp,
            "isolate rhythm",
            "rhythm",
            "Improved groove consistency before adding lyrics.",
            accompaniment_task=replace(
                task, rhythm_consistency=min(10, task.rhythm_consistency + 3)
            ),
        )

    def _copy(
        self, exp: CoordinationExperiment, name: str, slug: str, summary: str, **changes: object
    ) -> CoordinationExperiment:
        record = CoordinationExperimentRecord(name, exp.profile.identifier, summary)
        return CoordinationExperiment(
            replace(
                exp.profile,
                identifier=f"{exp.profile.identifier}-{slug}",
                **changes,  # type: ignore[arg-type]
            ),
            exp.history + (record,),
        )


class TempoLadderService:
    """Generate gradual tempo ladders."""

    def generate(self, start_bpm: int, target_bpm: int, step_bpm: int = 6) -> TempoLadder:
        if start_bpm <= 0 or target_bpm <= 0 or step_bpm <= 0:
            raise ValueError("Tempo ladder values must be positive.")
        tempos = [start_bpm]
        current = start_bpm
        while current < target_bpm:
            current = min(target_bpm, current + step_bpm)
            tempos.append(current)
        while current > target_bpm:
            current = max(target_bpm, current - step_bpm)
            tempos.append(current)
        return TempoLadder(
            start_bpm,
            target_bpm,
            step_bpm,
            tuple(tempos),
            "Gradual tempo increases preserve coordination success while adding only one "
            "new pressure at a time.",
        )
