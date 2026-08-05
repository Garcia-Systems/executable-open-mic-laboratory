"""Original-music presentation models for Chapter 13."""

from dataclasses import dataclass
from enum import Enum

from open_mic_lab.domain.validation import require_positive_int, require_rating, require_text


class FamiliarityStrategy(Enum):
    """Ways to orient listeners who have not heard the song before."""

    BRIEF_CONTEXT = "brief context"
    PERSONAL_STORY = "personal story"
    FAMILIAR_ANCHOR = "familiar anchor"
    AUDIENCE_PARTICIPATION = "audience participation"
    NO_EXPLANATION = "no explanation"


@dataclass(frozen=True, slots=True)
class OriginalWork:
    """A performer's original work as presented live, not songwriting mechanics."""

    identifier: str
    title: str
    themes: tuple[str, ...]
    accessibility_notes: str
    emotional_directness: int
    audience_participation_potential: int

    def __post_init__(self) -> None:
        require_text(self.identifier, "Original work identifier")
        require_text(self.title, "Original work title")
        require_text(self.accessibility_notes, "Original work accessibility notes")
        if not self.themes:
            raise ValueError("Original works need at least one reflective theme.")
        for theme in self.themes:
            require_text(theme, "Original work theme")
        require_rating_value(self.emotional_directness, "Emotional directness")
        require_rating_value(self.audience_participation_potential, "Participation potential")


@dataclass(frozen=True, slots=True)
class PerformanceContext:
    """Live context for presenting original material."""

    identifier: str
    venue_name: str
    completed_set_identifier: str
    performance_goal: str
    confidence_level: int

    def __post_init__(self) -> None:
        require_text(self.identifier, "Performance context identifier")
        require_text(self.venue_name, "Venue name")
        require_text(self.completed_set_identifier, "Completed set identifier")
        require_text(self.performance_goal, "Performance goal")
        require_rating_value(self.confidence_level, "Performance confidence")


@dataclass(frozen=True, slots=True)
class AudienceContext:
    """Audience context focused on expectations for unfamiliar material."""

    identifier: str
    profile_identifier: str
    expected_familiarity_need: int
    storytelling_receptiveness: int
    participation_receptiveness: int

    def __post_init__(self) -> None:
        require_text(self.identifier, "Audience context identifier")
        require_text(self.profile_identifier, "Audience profile identifier")
        require_rating_value(self.expected_familiarity_need, "Expected familiarity need")
        require_rating_value(self.storytelling_receptiveness, "Storytelling receptiveness")
        require_rating_value(self.participation_receptiveness, "Participation receptiveness")


@dataclass(frozen=True, slots=True)
class SongIntroduction:
    """Planned spoken framing before an original song."""

    identifier: str
    work_identifier: str
    strategy: FamiliarityStrategy
    duration_seconds: int
    story_theme: str | None = None

    def __post_init__(self) -> None:
        require_text(self.identifier, "Song introduction identifier")
        require_text(self.work_identifier, "Song introduction work identifier")
        require_positive_int(self.duration_seconds, "Song introduction duration")
        if self.story_theme is not None:
            require_text(self.story_theme, "Story theme")


@dataclass(frozen=True, slots=True)
class ArtisticIdentity:
    """Reflective identity tools, not creativity measurements."""

    identifier: str
    musical_themes: tuple[str, ...]
    recurring_styles: tuple[str, ...]
    audience_expectations: tuple[str, ...]
    repertoire_consistency_notes: str

    def __post_init__(self) -> None:
        require_text(self.identifier, "Artistic identity identifier")
        require_text(self.repertoire_consistency_notes, "Repertoire consistency notes")
        for label, values in (
            ("Musical themes", self.musical_themes),
            ("Recurring styles", self.recurring_styles),
            ("Audience expectations", self.audience_expectations),
        ):
            if not values:
                raise ValueError(f"{label} require at least one reflective entry.")
            for value in values:
                require_text(value, label[:-1])


@dataclass(frozen=True, slots=True)
class OriginalPresentationPlan:
    """Complete immutable plan for inserting originals into a set."""

    identifier: str
    setlist_identifier: str
    ordered_version_identifiers: tuple[str, ...]
    original_version_identifiers: tuple[str, ...]
    introductions: tuple[SongIntroduction, ...]
    context: PerformanceContext
    audience_context: AudienceContext
    artistic_identity: ArtisticIdentity
    notes: str = ""

    def __post_init__(self) -> None:
        require_text(self.identifier, "Original presentation plan identifier")
        require_text(self.setlist_identifier, "Set-list identifier")
        if not self.ordered_version_identifiers:
            raise ValueError("Original presentation plans require at least one song.")
        for version_id in self.ordered_version_identifiers + self.original_version_identifiers:
            require_text(version_id, "Presentation plan version identifier")
        missing = set(self.original_version_identifiers) - set(self.ordered_version_identifiers)
        if missing:
            raise ValueError("Original version identifiers must appear in the planned order.")


def require_rating_value(value: int, label: str) -> None:
    """Validate integer 0-10 educational ratings."""
    require_rating(__import__("decimal").Decimal(value), label)
