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

## Quality checks

```bash
pytest
ruff check .
ruff format --check .
mypy src
```

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
