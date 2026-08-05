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
