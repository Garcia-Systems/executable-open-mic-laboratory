"""Stage-presence communication models for Chapter 7."""

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from open_mic_lab.domain.validation import (
    require_non_negative_int,
    require_positive_int,
    require_rating,
    require_text,
)


class StageMoment(Enum):
    """Moments where the audience receives communication signals."""

    BEFORE_SET = "before set"
    BEFORE_SONG = "before song"
    DURING_SONG = "during song"
    BETWEEN_SONGS = "between songs"
    AFTER_SONG = "after song"
    AFTER_SET = "after set"


class IntroductionPurpose(Enum):
    """Educational purpose for a spoken introduction."""

    CONTEXT = "context"
    CONNECTION = "connection"
    ORIENTATION = "orientation"
    GRATITUDE = "gratitude"
    PARTICIPATION = "participation"


class EmotionalTone(Enum):
    """Tone communicated by a spoken segment."""

    WARM = "warm"
    PLAYFUL = "playful"
    REFLECTIVE = "reflective"
    CONFIDENT = "confident"
    VULNERABLE = "vulnerable"


class AudienceFamiliarity(Enum):
    """How familiar the audience is expected to be with the song."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PerformerBehavior(Enum):
    """Intentional non-musical communication behaviors."""

    GROUNDED_POSTURE = "grounded posture"
    EYE_CONTACT = "eye contact"
    SMILE = "smile"
    PURPOSEFUL_MOVEMENT = "purposeful movement"
    LISTENING_SILENCE = "listening silence"
    RECOVERY_BREATH = "recovery breath"
    AUDIENCE_INVITATION = "audience invitation"


@dataclass(frozen=True, slots=True)
class StorySegment:
    """A short story attached to an introduction."""

    theme: str
    estimated_duration_seconds: int
    personal: bool
    connects_to_song: bool

    def __post_init__(self) -> None:
        require_text(self.theme, "Story theme")
        require_positive_int(self.estimated_duration_seconds, "Story duration")


@dataclass(frozen=True, slots=True)
class SpokenIntroduction:
    """Structured spoken introduction rather than plain text."""

    identifier: str
    song_version_identifier: str
    purpose: IntroductionPurpose
    estimated_duration_seconds: int
    emotional_tone: EmotionalTone
    audience_familiarity: AudienceFamiliarity
    transition_target: str
    story: StorySegment | None = None

    @property
    def total_duration_seconds(self) -> int:
        """Return spoken duration including an optional story."""
        story_seconds = 0 if self.story is None else self.story.estimated_duration_seconds
        return self.estimated_duration_seconds + story_seconds

    def __post_init__(self) -> None:
        require_text(self.identifier, "Introduction identifier")
        require_text(self.song_version_identifier, "Introduction song version identifier")
        require_positive_int(self.estimated_duration_seconds, "Introduction duration")
        require_text(self.transition_target, "Introduction transition target")


@dataclass(frozen=True, slots=True)
class AudienceInteraction:
    """Planned audience interaction at a specific performance moment."""

    identifier: str
    moment: StageMoment
    description: str
    estimated_duration_seconds: int
    participation_level: int
    optional: bool = True

    def __post_init__(self) -> None:
        require_text(self.identifier, "Audience interaction identifier")
        require_text(self.description, "Audience interaction description")
        require_non_negative_int(self.estimated_duration_seconds, "Audience interaction duration")
        require_rating(Decimal(self.participation_level), "Audience participation level")


@dataclass(frozen=True, slots=True)
class PerformanceFlow:
    """Timing and behavior choices around a set."""

    silence_between_songs_seconds: tuple[int, ...]
    transition_smoothness: int
    confidence_continuity: int
    eye_contact_opportunities: int
    storytelling_opportunities: int
    recovery_plan: str
    behaviors: tuple[PerformerBehavior, ...]

    def __post_init__(self) -> None:
        if not self.silence_between_songs_seconds:
            raise ValueError("Performance flow requires silence estimates")
        for silence in self.silence_between_songs_seconds:
            require_non_negative_int(silence, "Silence between songs")
        require_rating(Decimal(self.transition_smoothness), "Transition smoothness")
        require_rating(Decimal(self.confidence_continuity), "Confidence continuity")
        require_non_negative_int(self.eye_contact_opportunities, "Eye-contact opportunities")
        require_non_negative_int(self.storytelling_opportunities, "Storytelling opportunities")
        require_text(self.recovery_plan, "Recovery plan")


@dataclass(frozen=True, slots=True)
class CommunicationPlan:
    """Complete stage-presence communication plan for one performance."""

    identifier: str
    setlist_identifier: str
    available_spoken_seconds: int
    introductions: tuple[SpokenIntroduction, ...]
    interactions: tuple[AudienceInteraction, ...]
    flow: PerformanceFlow
    notes: str = ""

    @property
    def planned_spoken_seconds(self) -> int:
        """Return total planned spoken and interaction time."""
        return sum(intro.total_duration_seconds for intro in self.introductions) + sum(
            interaction.estimated_duration_seconds for interaction in self.interactions
        )

    def __post_init__(self) -> None:
        require_text(self.identifier, "Communication plan identifier")
        require_text(self.setlist_identifier, "Communication plan setlist identifier")
        require_positive_int(self.available_spoken_seconds, "Available spoken time")
