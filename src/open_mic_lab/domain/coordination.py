"""Chapter 5 domain objects for singing while playing."""

from dataclasses import dataclass

from open_mic_lab.domain.validation import require_int_between, require_positive_int, require_text


@dataclass(frozen=True, slots=True)
class VocalTask:
    """The singing task competing for the learner's attention."""

    lyric_familiarity: int
    vocal_confidence: int
    breathing_complexity: int

    def __post_init__(self) -> None:
        require_int_between(self.lyric_familiarity, "Lyric familiarity", 0, 10)
        require_int_between(self.vocal_confidence, "Vocal confidence", 0, 10)
        require_int_between(self.breathing_complexity, "Breathing complexity", 0, 10)


@dataclass(frozen=True, slots=True)
class AccompanimentTask:
    """The instrumental task competing for the learner's attention."""

    accompaniment_difficulty: int
    arrangement_complexity: int
    chord_transition_security: int
    rhythm_consistency: int

    def __post_init__(self) -> None:
        require_int_between(self.accompaniment_difficulty, "Accompaniment difficulty", 0, 10)
        require_int_between(self.arrangement_complexity, "Arrangement complexity", 0, 10)
        require_int_between(self.chord_transition_security, "Chord transition security", 0, 10)
        require_int_between(self.rhythm_consistency, "Rhythm consistency", 0, 10)


@dataclass(frozen=True, slots=True)
class Automaticity:
    """How much of the task can run with reduced conscious attention."""

    accompaniment: int
    lyrics: int
    coordination: int

    def __post_init__(self) -> None:
        require_int_between(self.accompaniment, "Accompaniment automaticity", 0, 10)
        require_int_between(self.lyrics, "Lyric automaticity", 0, 10)
        require_int_between(self.coordination, "Coordination automaticity", 0, 10)


@dataclass(frozen=True, slots=True)
class CognitiveLoad:
    """Educational estimate of how much attention a performance version demands."""

    score: int
    category: str
    explanation: str

    def __post_init__(self) -> None:
        require_int_between(self.score, "Cognitive load", 0, 100)
        require_text(self.category, "Cognitive load category")
        require_text(self.explanation, "Cognitive load explanation")


@dataclass(frozen=True, slots=True)
class CoordinationProfile:
    """Inputs for deterministic coordination analysis."""

    identifier: str
    vocal_task: VocalTask
    accompaniment_task: AccompanimentTask
    automaticity: Automaticity
    tempo_bpm: int
    target_tempo_bpm: int
    hand_voice_independence: int
    recent_practice_minutes: int

    def __post_init__(self) -> None:
        require_text(self.identifier, "Coordination profile identifier")
        require_positive_int(self.tempo_bpm, "Tempo")
        require_positive_int(self.target_tempo_bpm, "Target tempo")
        require_int_between(self.hand_voice_independence, "Hand/voice independence", 0, 10)
        if self.recent_practice_minutes < 0:
            raise ValueError("Recent practice minutes cannot be negative.")


@dataclass(frozen=True, slots=True)
class CoordinationExperimentRecord:
    """One immutable coordination practice experiment."""

    name: str
    source_profile_identifier: str
    summary: str

    def __post_init__(self) -> None:
        require_text(self.name, "Coordination experiment name")
        require_text(self.source_profile_identifier, "Source coordination profile")
        require_text(self.summary, "Coordination experiment summary")


@dataclass(frozen=True, slots=True)
class CoordinationExperiment:
    """Copied profile plus history for comparing practice experiments."""

    profile: CoordinationProfile
    history: tuple[CoordinationExperimentRecord, ...] = ()
