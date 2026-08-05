# Volume I Overview

Volume I guides a learner from first motivation through repeated live performances and continuous improvement.

## Educational philosophy

The laboratory is deterministic, transparent, and learner-centered. Scores are educational summaries, not measurements of talent or artistic worth. Every recommendation includes a reason so learners can accept, reject, or revise it.

## Subsystem architecture

```mermaid
flowchart TD
    Ch0[Readiness] --> Ch1[Song Choice]
    Ch1 --> Ch2[Repertoire]
    Ch2 --> Ch3[Set Building]
    Ch3 --> Ch4[Arrangements]
    Ch4 --> Ch5[Coordination]
    Ch5 --> Ch6[Practice]
    Ch6 --> Ch7[Communication]
    Ch7 --> Ch8[Equipment]
    Ch8 --> Ch9[Sound Check]
    Ch9 --> Ch10[Audience]
    Ch10 --> Ch11[Recovery]
    Ch11 --> Ch12[Improvisation]
    Ch12 --> Ch13[Originals]
    Ch13 --> Ch14[Open Mic Event]
    Ch14 --> Ch15[Analytics]
```

Core packages remain stable: `domain` contains immutable educational concepts, `services` contain deterministic calculations, `sample_data` provides repeatable examples, `cli` exposes laboratories, and `debug_labs` supports step-through learning.

## Chapter progression

Chapters 0–15 are implemented. The capstone, Chapter 15, connects repertoire, readiness, arrangements, practice, coordination, communication, equipment, sound check, audience observations, recovery, improvisation, original music, and event summaries into continuous improvement.

## Deterministic simulation approach

The repository uses fictional/public-domain-style data and deterministic calculations so examples, tests, CLI output, and debugging sessions are repeatable.

## Debugging workflow

Each debug lab rebuilds sample data from a known baseline. Launch configurations make it possible to inspect variables at documented breakpoint markers without network access or hidden state.

## Future extension points

Possible future extensions include persistence, richer dashboards, notebooks, media integrations, or AI-assisted reflection. They are intentionally not part of the completed Volume I implementation.
