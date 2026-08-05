# Executable Open Mic Laboratory

An executable textbook for adult musicians learning to become more compelling live performers through repertoire engineering, deliberate practice, performance simulation, audience awareness, reflection, and experimentation.

## Vision

Live performance is an interconnected system. The central question is: **“What happens if I change this?”** Change a key, tempo, instrument, introduction, set-list order, vocal comfort rating, or recovery skill and compare the result.

## Current milestone

Milestone 1 establishes the Python 3.12 foundation: dataclass domain objects, deterministic sample data, educational readiness scoring, set-list analysis, an argparse CLI, docs, tests, ruff, and mypy.

## Features

- Separate `Song` and `PerformanceVersion` models.
- Repertoire validation for duplicate identifiers and unknown song references.
- 0-100 readiness scores with human-readable breakdowns.
- Friendly set-list duration, contrast, and closer warnings.
- Deterministic fictional/public-domain-style sample repertoire.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

## CLI examples

```bash
open-mic-lab repertoire list
open-mic-lab repertoire ready
open-mic-lab readiness show river-guitar-lowered
open-mic-lab setlist sample
open-mic-lab setlist analyze
open-mic-lab demo
python -m open_mic_lab.cli demo
```

## Continuous integration

The `CI` GitHub Actions workflow verifies every pull request targeting `main`, every push to `main`, and manual runs started with `workflow_dispatch`. It installs the package with development dependencies, then runs the automated test suite, Ruff linting, Ruff formatting checks, and mypy type checking on the supported Python versions.

Run the same checks locally with:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m pytest
ruff check .
ruff format --check .
mypy src
```

GitHub Actions creates status checks, but repository settings decide whether those checks are required before merging. To require CI for `main`, a repository owner can open GitHub repository **Settings**, open **Branches** or **Rules**, create a ruleset or branch-protection rule for `main`, require pull requests before merging, require status checks to pass, select the `Verification (Python 3.12)` and `Verification (Python 3.14)` checks from the `CI` workflow, and optionally require branches to be up to date before merging.

## Project structure

```text
docs/                 Architecture notes and executable textbook chapters.
examples/             Small runnable examples.
src/open_mic_lab/     Package, CLI, domain objects, services, sample data.
tests/                Behavior-focused pytest suite.
```

## Educational disclaimer

This project does not evaluate artistic worth. Readiness scores are educational comparisons, not predictions. Audience-response measures are subjective, and this software does not guarantee a successful performance.

## Roadmap

Later chapters may add persistence, analytics, MIDI/audio integrations, notebooks, dashboards, AI-assisted reflection, and richer laboratories when they are needed.

## Contributing

Keep the core deterministic, typed, dependency-light, and learner-friendly. Prefer small domain objects and isolated services over hidden global state.

## Chapter 1: Song Suitability Laboratory

Chapter 1, **Choosing Songs**, is implemented in `docs/chapters/chapter-01-choosing-songs.md`. It adds a deterministic laboratory for comparing candidate performance versions for a specific performer, venue, audience, and moment. The score is a transparent educational fit score, not a ranking of artistic quality.

New examples:

```bash
open-mic-lab songs scenarios
open-mic-lab songs evaluate harbor-guitar --scenario coffeehouse
open-mic-lab songs compare --scenario coffeehouse
open-mic-lab songs compare --scenario listening-room
open-mic-lab songs explain window-guitar-original-feature --scenario first-performance
open-mic-lab chapter-one-demo
```

The laboratory includes transposition and simplification experiments. These create copied `PerformanceVersion` objects rather than mutating repertoire data. Lowering a key shifts the modeled vocal range by the same semitone interval; simplification lowers arrangement difficulty and applies a bounded projected accompaniment-stability change. Both are educational assumptions, not measured musical facts.

Song rankings have explicit limitations: vocal range is not vocal health, familiarity is contextual, personal connection is subjective, and a lower-scoring choice may still be the right artistic decision for a particular night.

## Roadmap status

Implemented: Chapter 0 foundations and Chapter 1 song choice experiments. Deferred to Chapter 2 or later: full repertoire database, persistence, graphical dashboards, audio analysis, AI recommendations, and advanced set-list optimization.

## Chapter 2 — Repertoire Engineering

Chapter 2 turns the sample repertoire into a decision-support system. Use `open-mic-lab repertoire summary`, `gaps`, `health`, `priorities`, `neglected`, and `diversity` to inspect balance, stalled songs, missing set roles, and learning priorities. The chapter builds on Chapter 0 readiness and Chapter 1 suitability, then prepares Chapter 3 to use repertoire evidence in fuller performance planning.


## Chapter 3 — Building a Set

Chapter 3 extends the lab from individual songs and repertoire health to complete performance flow. It introduces first-class transitions, deterministic timeline generation, set analysis, neutral set comparison, immutable set experiments, sample scenarios, a CLI demo, and a debug lab.

Useful commands:

```bash
open-mic-lab set summary
open-mic-lab set timeline
open-mic-lab set analyze
open-mic-lab set compare
open-mic-lab set experiment swap harbor-guitar window-piano
open-mic-lab chapter-three-demo
python -m open_mic_lab.debug_labs.chapter_03_building_a_set
```

Set construction builds on Chapter 2 repertoire engineering by sequencing prepared songs for a venue, and prepares Chapter 4 by making arrangement tradeoffs easier to hear in context.

## Chapter 4 — Making Songs Your Own

Chapter 4 introduces dedicated `Arrangement` objects so learners can change key, tempo, instrument, groove, form, simplification, dynamics, and audience cues without rewriting the underlying `Song` or erasing the prepared `PerformanceVersion`. Arrangement experiments are immutable and carry history records.

Useful commands:

```bash
open-mic-lab arrangement list
open-mic-lab arrangement compare
open-mic-lab arrangement analyze
open-mic-lab arrangement experiment transpose window-piano-arrangement G -2
open-mic-lab arrangement experiment simplify window-piano-arrangement
open-mic-lab arrangement experiment tempo window-piano-arrangement 64
open-mic-lab arrangement experiment groove window-piano-arrangement coffeehouse
open-mic-lab arrangement history
open-mic-lab chapter-four-demo
python -m open_mic_lab.debug_labs.chapter_04_arrangements
```

Chapter 4 prepares Chapter 5 by making intentional arrangement choices observable before the learner studies how those choices land with an audience.
