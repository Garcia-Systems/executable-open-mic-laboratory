# Source-to-System Map

This map links research and professional foundations to executable parts of the repository. It is intentionally conceptual: sources motivate concepts, while implementation formulas remain repository-designed heuristics.

## Chapter and service mapping

| Area | Evidence base | Service or model | Chapter | CLI / demo | Debug lab |
|---|---|---|---|---|---|
| Performance readiness | Music performance preparation; feedback; reflection | `ReadinessResult`, `calculate_readiness` | Chapter 0 | `readiness`, `demo` | `chapter_00_readiness.py` |
| Song fit and repertoire choice | Expertise, repertoire selection, performer-task fit | `SongSuitabilityService` | Chapter 1 | `songs`, `chapter-one-demo` | `chapter_01_song_suitability.py` |
| Repertoire management | Deliberate practice, self-regulated planning | `RepertoireEngineeringService` | Chapter 2 | `repertoire` | `chapter_02_repertoire_engineering.py` |
| Set sequencing | Programming practice; attention and contrast | `SetBuilderService`, `analyze_setlist` | Chapter 3 | `set`, `setlist` | `chapter_03_building_a_set.py` |
| Arrangement and adaptation | Interpretation, creative adaptation, performer fit | `ArrangementAnalysisService` | Chapter 4 | `arrangements` | `chapter_04_arrangements.py` |
| Singing while playing | Cognitive load, divided attention, automaticity | `CoordinationAnalysisService` | Chapter 5 | `coordination` | `chapter_05_coordination.py` |
| Deliberate practice | Deliberate practice, feedback, self-regulation | `PracticePlanningService` | Chapter 6 | `practice` | `chapter_06_practice_engineering.py` |
| Stage presence | Visual perception, movement, audience engagement | `CommunicationAnalysisService` | Chapter 7 | `stage` | `chapter_07_stage_presence.py` |
| Signal flow | Audio engineering and live-sound practice | `SignalFlowService` | Chapter 8 | `equipment` | `chapter_08_signal_flow.py` |
| Soundcheck | Gain structure, monitoring, feedback control | `SoundCheckService` | Chapter 9 | `soundcheck` | `chapter_09_sound_check.py` |
| Audience experience | Music cognition, participation, concert experience | `AudienceResponseService` | Chapter 10 | `audience` | `chapter_10_audience_experience.py` |
| Recovery | Coping, interruption recovery, reflective practice | `RecoveryAnalysisService` | Chapter 11 | `recovery` | `chapter_11_recovery.py` |
| Improvisation | Improvisation, constraints, adaptive expertise | `ImprovisationAnalysisService` | Chapter 12 | `improvisation` | `chapter_12_improvisation.py` |
| Original music | Artistic identity, audience familiarity, framing | `OriginalMusicAnalysisService` | Chapter 13 | `originals` | `chapter_13_original_music.py` |
| Open-mic simulation | Experiential learning and simulation-based learning | `OpenMicEventService` | Chapter 14 | `event`, `chapter-fourteen-demo` | `chapter_14_open_mic.py` |
| Analytics and improvement | Reflection, feedback, continuous improvement | `PerformanceAnalyticsService` | Chapter 15 | `analytics` | `chapter_15_performance_analytics.py` |

## Formula status

Every score in these services is an **Educational Heuristic** unless a docstring explicitly says otherwise. No service claims that research proves its exact weights, thresholds, or numerical output.
