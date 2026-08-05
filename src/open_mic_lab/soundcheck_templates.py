"""Deterministic Chapter 9 sound-check templates and venue profiles."""

from open_mic_lab.domain.soundcheck import (
    ChannelSettings,
    EQProfile,
    MixerSettings,
    MonitorMix,
    SoundCheck,
    VenueAcoustics,
)


def venue_profiles() -> dict[str, VenueAcoustics]:
    """Return educational venue approximations, not acoustic measurements."""
    return {
        "quiet-coffeehouse": VenueAcoustics(
            "quiet-coffeehouse",
            "Quiet Coffeehouse",
            "small",
            2,
            4,
            5,
            4,
            ("Soft room where lyric clarity matters.",),
        ),
        "noisy-cafe": VenueAcoustics(
            "noisy-cafe",
            "Noisy Café",
            "small",
            7,
            5,
            4,
            6,
            ("Background noise tempts the performer to over-amplify.",),
        ),
        "church-sanctuary": VenueAcoustics(
            "church-sanctuary",
            "Church Sanctuary",
            "large",
            3,
            8,
            6,
            7,
            ("Reflective space where monitors and high mids need restraint.",),
        ),
        "outdoor-event": VenueAcoustics(
            "outdoor-event",
            "Outdoor Event",
            "open",
            6,
            1,
            2,
            3,
            ("Little room reflection, but audience coverage is uneven.",),
        ),
        "rehearsal-room": VenueAcoustics(
            "rehearsal-room",
            "Rehearsal Room",
            "small",
            4,
            7,
            2,
            8,
            ("Tight reflective room with high feedback sensitivity.",),
        ),
        "community-center": VenueAcoustics(
            "community-center",
            "Community Center",
            "medium",
            5,
            5,
            7,
            5,
            ("Absorptive audience can make the house feel different after doors open.",),
        ),
    }


def default_mixer_settings() -> MixerSettings:
    return MixerSettings(
        (
            ChannelSettings(
                "ch1",
                "Lead Vocal",
                "vocal-mic",
                6,
                6,
                EQProfile(0, 1, 0, "clear lyric EQ"),
                microphone_distance_cm=12,
            ),
            ChannelSettings(
                "ch2", "Piano", "digital-piano", 5, 7, EQProfile(0, 0, 0, "flat piano EQ")
            ),
            ChannelSettings(
                "ch3",
                "Unused Guest Mic",
                "guest-mic",
                0,
                0,
                EQProfile(),
                muted=True,
                microphone_distance_cm=20,
            ),
        ),
        MonitorMix(vocal_level=6, accompaniment_level=4, overall_level=3),
        master_level=6,
    )


def sample_soundcheck(venue_id: str = "noisy-cafe") -> SoundCheck:
    venues = venue_profiles()
    return SoundCheck(
        "chapter-09-soundcheck",
        "Avery",
        "piano-and-vocal",
        venues[venue_id],
        default_mixer_settings(),
    )
