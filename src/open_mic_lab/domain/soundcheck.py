"""Sound-check domain models for Chapter 9."""

from dataclasses import dataclass
from enum import Enum

from open_mic_lab.domain.validation import require_text


class FeedbackRisk(Enum):
    """Educational feedback-risk categories."""

    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"


class BalanceAssessment(Enum):
    """Simple mix-balance labels for learners."""

    TOO_QUIET = "too quiet"
    SLIGHTLY_QUIET = "slightly quiet"
    BALANCED = "balanced"
    SLIGHTLY_LOUD = "slightly loud"
    TOO_LOUD = "too loud"
    MUTED = "muted"


@dataclass(frozen=True, slots=True)
class EQProfile:
    """Coarse educational EQ choices, measured in small relative steps."""

    low: int = 0
    mid: int = 0
    high: int = 0
    note: str = "flat educational EQ"


@dataclass(frozen=True, slots=True)
class ChannelSettings:
    """Settings for one mixer channel."""

    channel_id: str
    label: str
    source_node: str
    gain: int
    fader: int
    eq: EQProfile = EQProfile()
    muted: bool = False
    microphone_distance_cm: int | None = None

    def __post_init__(self) -> None:
        require_text(self.channel_id, "Channel identifier")
        require_text(self.label, "Channel label")
        require_text(self.source_node, "Channel source node")
        if not 0 <= self.gain <= 10:
            raise ValueError("Channel gain must be between 0 and 10.")
        if not 0 <= self.fader <= 10:
            raise ValueError("Channel fader must be between 0 and 10.")
        if self.microphone_distance_cm is not None and self.microphone_distance_cm <= 0:
            raise ValueError("Microphone distance must be positive when provided.")


@dataclass(frozen=True, slots=True)
class MonitorMix:
    """Performer's simplified monitor mix."""

    vocal_level: int
    accompaniment_level: int
    overall_level: int

    def __post_init__(self) -> None:
        for name, value in (
            ("Monitor vocal level", self.vocal_level),
            ("Monitor accompaniment level", self.accompaniment_level),
            ("Monitor overall level", self.overall_level),
        ):
            if not 0 <= value <= 10:
                raise ValueError(f"{name} must be between 0 and 10.")


@dataclass(frozen=True, slots=True)
class MixerSettings:
    """Complete learner-facing mixer state."""

    channels: tuple[ChannelSettings, ...]
    monitor_mix: MonitorMix
    master_level: int = 6

    def __post_init__(self) -> None:
        if len({channel.channel_id for channel in self.channels}) != len(self.channels):
            raise ValueError("Mixer channels must have unique identifiers.")
        if not 0 <= self.master_level <= 10:
            raise ValueError("Master level must be between 0 and 10.")


@dataclass(frozen=True, slots=True)
class VenueAcoustics:
    """Educational approximation of a venue, not a physics model."""

    identifier: str
    name: str
    room_size: str
    noise_level: int
    reflectivity: int
    audience_absorption: int
    monitor_sensitivity: int
    notes: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        require_text(self.identifier, "Venue profile identifier")
        require_text(self.name, "Venue profile name")
        require_text(self.room_size, "Venue room size")
        for name, value in (
            ("Noise level", self.noise_level),
            ("Reflectivity", self.reflectivity),
            ("Audience absorption", self.audience_absorption),
            ("Monitor sensitivity", self.monitor_sensitivity),
        ):
            if not 0 <= value <= 10:
                raise ValueError(f"{name} must be between 0 and 10.")


@dataclass(frozen=True, slots=True)
class SoundCheck:
    """A repeatable sound-check configuration."""

    identifier: str
    performer: str
    signal_path_id: str
    venue: VenueAcoustics
    mixer_settings: MixerSettings

    def __post_init__(self) -> None:
        require_text(self.identifier, "Sound check identifier")
        require_text(self.performer, "Performer")
        require_text(self.signal_path_id, "Signal path identifier")
