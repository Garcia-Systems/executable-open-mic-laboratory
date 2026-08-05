"""Reflection model."""

from dataclasses import dataclass

from open_mic_lab.domain.validation import require_text


@dataclass(frozen=True, slots=True)
class Reflection:
    """Structured reflection after a performance."""

    performance_identifier: str
    surprises: str
    what_felt_easy: str
    what_felt_difficult: str
    audience_response: str
    transitions_that_worked: str
    stories_that_connected: str
    planned_change_for_next_time: str

    def __post_init__(self) -> None:
        require_text(self.performance_identifier, "Performance identifier")
        require_text(self.planned_change_for_next_time, "Planned change for next time")
