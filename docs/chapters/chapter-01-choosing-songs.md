# Chapter 1 — Choosing Songs

## Learning objectives

By the end of the chapter, the learner should be able to explain why personal taste alone does not determine performance suitability; distinguish a song from a performer-specific version; identify hard constraints and soft preferences; evaluate vocal, technical, emotional, audience, and venue fit; interpret a transparent suitability score; compare songs without treating the ranking as artistic truth; test adaptations such as transposition and simplification; and select a song deliberately for a specific performance opportunity.

## Narrative introduction

Musicians often choose songs because they love the recording, the song is impressive, friends know it, it showcases technique, or it feels emotionally meaningful. Each reason can be valuable, but none alone guarantees that the song will work in the room.

A performance song is not just a composition. It is a relationship among the song, performer, arrangement, venue, audience, and moment.

```mermaid
flowchart LR
    S[Song] --> V[Performance Version]
    P[Performer Profile] --> E[Suitability Evaluation]
    V --> E
    A[Audience] --> E
    N[Venue] --> E
    R[Current Readiness] --> E
    E --> C[Candidate Comparison]
    C --> X[Experiment]
    X --> V2[Revised Performance Version]
```

## Laboratory

Evaluate one song:

```bash
open-mic-lab songs evaluate harbor-guitar --scenario coffeehouse
```

Compare candidates:

```bash
open-mic-lab songs compare --scenario coffeehouse
open-mic-lab songs compare --scenario listening-room
```

Identify a hard constraint by comparing piano songs in a guitar-only scenario, then examine missing information through the completeness percentage:

```bash
open-mic-lab songs explain lantern-piano --scenario first-performance
```

Transpose and simplify in Python:

```python
from open_mic_lab.sample_data import (
    build_sample_repertoire,
    sample_selection_scenarios,
    sample_selection_venue,
)
from open_mic_lab.services.experiment_service import PerformanceVersionExperimentService
from open_mic_lab.services.suitability_service import SongSuitabilityService

rep = build_sample_repertoire()
profile = sample_selection_scenarios()["coffeehouse"]
venue = sample_selection_venue(profile.venue_identifier)
version = rep.get_version("window-guitar-original-feature")
experiments = PerformanceVersionExperimentService()
lowered = experiments.transpose(version, "F", -2)
simplified = experiments.simplify(version)
service = SongSuitabilityService()
print(service.evaluate(version, rep, profile, venue).score)
print(service.evaluate(lowered, rep, profile, venue).score)
print(service.evaluate(simplified, rep, profile, venue).score)
```

Compare the revised version with the original, interpret tradeoffs, and choose a candidate by explaining why its strengths matter for this opportunity. The laboratory can show that a familiar audience favorite scores differently from a personally meaningful original, but it cannot decide your artistic intention.

## Reflection questions

- Which song do you enjoy practicing most?
- Which song feels safest?
- Which song best introduces you to an unfamiliar audience?
- Which song creates the strongest emotional connection?
- Which weaknesses could be adapted rather than accepted?
- What information does the laboratory not know about you?
- Would you choose the highest-scoring song? Why or why not?
- What would you change before performing the song?

## Limitations

Scores do not measure artistic quality. Audience familiarity is contextual and subjective. Vocal range does not measure vocal tone, fatigue, or healthy technique. Adaptation estimates are educational scenarios. Personal connection cannot be fully represented numerically. A surprising artistic choice may work even when a model considers it risky.

## Chapter summary

Choose songs for a particular performer, audience, venue, and moment—not in the abstract.

## Debug Laboratory

The Chapter 1 executable laboratory prints suitability scores. The debug laboratory pauses a focused scenario so you can trace why one version fits a particular opportunity better than another, then inspect how an adaptation changes the result without mutating the original object.

Use the VS Code launch configuration **Debug Chapter 1 Song Suitability Lab**, or run the same helper from the repository root:

```bash
python -m open_mic_lab.debug_labs.chapter_01_song_suitability
```

Recommended breakpoint markers are in `src/open_mic_lab/debug_labs/chapter_01_song_suitability.py`:

1. `BREAKPOINT: Inspect the profile, hard constraints, soft preferences, weights, and candidates.`
2. `BREAKPOINT: Step Into the suitability service for Candidate A.`
3. `BREAKPOINT: Step Into the suitability service for Candidate B and inspect criteria.`
4. `BREAKPOINT: Inspect stable ranking and tie-breaking in the comparison result.`
5. `BREAKPOINT: Step Into the experiment service and confirm it returns a copied version.`
6. `BREAKPOINT: Confirm the source object is unchanged, then reevaluate the adapted copy.`

Inspect these variables: `scenario`, `venue`, `candidate_a`, `candidate_b`, `candidate_b_original_key`, `candidate_a_readiness`, `candidate_b_readiness`, `candidate_a_result`, `candidate_b_result`, `adapted_candidate_b`, `adapted_candidate_b_result`, `comparison`, `adapted_comparison`, `source_candidate_was_mutated`, and `score_change`.

Step Into these functions while stopped at the marked lines: `calculate_readiness`, `SongSuitabilityService.evaluate`, `SongSuitabilityService.compare`, and `PerformanceVersionExperimentService.transpose`.

Useful Watch expressions:

```python
candidate_a_result.score
candidate_b_result.score
candidate_b_result.completeness
candidate_b_result.concerns
adapted_candidate_b is candidate_b
adapted_candidate_b.performance_key
adapted_candidate_b_result.score
comparison.results[0].version_id
source_candidate_was_mutated
score_change
```

Questions to answer:

- Why does Candidate A score higher in this scenario?
- Is Candidate B rejected by a hard constraint or reduced by a soft preference?
- Which criteria are affected by transposition?
- Which criteria remain unchanged?
- How can a lower-ranked candidate still be the learner's preferred choice?
- How does stable tie-breaking make the simulation deterministic?
- How can you prove that the original object was not mutated?

Reset by stopping the debugger and launching the same configuration again. The helper rebuilds the repertoire, profile, venue, services, comparison, and adapted copy from deterministic sample data.

Expected conceptual finding: suitability is contextual rather than universal. Hard constraints can cap or exclude a candidate, soft preferences change weighted criteria, missing optional information lowers completeness, and the service explains its reasoning through a structured result rather than a bare score.
