# Debugging Guide

This repository treats debugging as an educational laboratory. Run commands when you want to observe a complete result; use a debug lab when you want to pause execution and inspect how the result is constructed.

## Development setup

From the repository root, install the project and development tools:

```bash
python -m pip install -e ".[dev]"
```

In VS Code, choose the Python interpreter for the environment where you installed the project. Open **Command Palette → Python: Select Interpreter**, then select the interpreter for this repository or dev container.

## Running a chapter debug lab in VS Code

1. Open the repository folder in VS Code.
2. Open **Run and Debug**.
3. Choose **Debug Chapter 0 Readiness Lab** or **Debug Chapter 1 Song Suitability Lab**.
4. Open the matching file in `src/open_mic_lab/debug_labs/`.
5. Place a breakpoint on the executable line immediately below a `BREAKPOINT:` marker.
6. Start debugging.

## Debug controls

- **Continue** runs until the next breakpoint or program end.
- **Step Over** executes the current line without entering called functions.
- **Step Into** enters a called function, such as a readiness or suitability service.
- **Step Out** finishes the current function and returns to the caller.

Use **Variables** to inspect local state, **Watch** to pin expressions from the chapter guide, and **Debug Console** to evaluate small expressions against the paused frame.

## Restarting deterministic scenarios

Stop the debugger and launch the same configuration again. Debug helpers rebuild sample data, services, and experiments with no network access and no user input, so the baseline is repeatable.

## Learning workflow

During a first walkthrough, avoid editing service code. First understand which domain objects enter the calculation, where validation has already happened, how criteria are weighted, and how the structured result explains the score. After you can explain the baseline, make one intentional change to sample data or an experiment and rerun the same debug lab.

## Future chapter convention

Every new chapter should normally include:

1. narrative explanation;
2. executable laboratory;
3. focused debug helper;
4. named VS Code launch configuration;
5. marked breakpoint locations;
6. variables or watch expressions to inspect;
7. guided questions;
8. deterministic reset path;
9. tests for the helper or underlying scenario;
10. documentation showing how the debug path connects to the chapter concept.

Name future debug helpers with chapter number plus concept, for example `chapter_02_repertoire_engineering.py`, `chapter_03_set_builder.py`, and `chapter_04_arrangement_experiments.py`. Do not create future chapter files before their chapter work begins.

## Chapter 2 Repertoire Engineering Debug Lab

Use VS Code launch configuration **Debug Chapter 2 Repertoire Engineering Lab** or run `python -m open_mic_lab.debug_labs.chapter_02_repertoire_engineering`. Breakpoint markers expose `repertoire`, `analysis`, `genre_distribution`, `key_distribution`, `neglected_version_ids`, `gaps`, `priorities`, `top_priority`, and `health`. Step into `RepertoireEngineeringService.analyze`, `gaps`, `priorities`, and `health` to see why recommendations are produced.


## Chapter 3 Building a Set Debug Lab

Use VS Code launch configuration **Debug Chapter 3 Building a Set Lab** or run `python -m open_mic_lab.debug_labs.chapter_03_building_a_set`. Breakpoint markers expose `candidate_set`, `transitions`, `timeline`, `cumulative_running_time`, `analysis`, `energy_observation`, `comparison`, `swapped_set`, `immutable_original_order`, and `experiment_order`. Step into `SetBuilderService.timeline`, `analyze`, `compare`, and `swap_songs` to observe how complete-set decisions are derived without mutating the original set.

## Chapter 4 Arrangements Debug Lab

Use VS Code launch configuration **Debug Chapter 4 Arrangements Lab** or run `python -m open_mic_lab.debug_labs.chapter_04_arrangements`. Breakpoint markers expose `original`, `source_version`, `transposed`, `immutable_original_key`, `simplified`, `shortened`, `slowed`, `experiment_history`, `comparison`, `timeline`, and `total_timeline_seconds`. Step into `ArrangementExperimentService`, `ArrangementAnalysisService.compare`, and `ArrangementTimelineService.timeline` to observe how arrangement decisions are copied, chained, compared, and timed without mutating the original arrangement.

## Chapter 5 coordination debug lab

Use the VS Code launch configuration named **Debug Chapter 5 Coordination Lab** or run:

```bash
python -m open_mic_lab.debug_labs.chapter_05_coordination
```

Suggested breakpoints:

- `baseline_analysis` to inspect coordination-score calculation.
- `bottlenecks` to inspect bottleneck ordering.
- `simplified` to confirm immutable experiment copies.
- `tempo_experiment` to compare reduced-tempo effects.
- `ladder` to inspect tempo ladder generation.

The lab is intentionally deterministic so repeated debugger runs expose the same variables and scores.

## Chapter 6 practice engineering debug lab

Use VS Code launch configuration **Debug Chapter 6 Practice Engineering Lab** or run:

```bash
python -m open_mic_lab.debug_labs.chapter_06_practice_engineering
```

Suggested breakpoints:

- `priorities` to inspect readiness, maintenance, learner-priority, and bottleneck scoring.
- `practice_plan` to inspect ordered blocks, duration allocation, and sequencing rationale.
- `maintenance_plan` to confirm adaptive experiments return new plans.
- `analytics` to inspect practice balance observations.

The lab connects Chapter 6 to Chapter 0 readiness, Chapter 2 repertoire maintenance, Chapter 4 arrangement decisions, and Chapter 5 coordination bottlenecks.


## Chapter 7 stage-presence debug lab

Use **Debug Chapter 7 Stage Presence Lab** in VS Code or run:

```bash
python -m open_mic_lab.debug_labs.chapter_07_stage_presence
```

Breakpoint markers guide you through communication-plan construction, structured introduction analysis, pacing evaluation, audience interaction analysis, immutable communication experiments, and before/after flow comparison. The useful variables are `plan`, `introduction_observations`, `flow_observations`, `shortened_plan`, `participation_plan`, and `comparison`.

## Chapter 8 Signal Flow Debug Lab

Run `python -m open_mic_lab.debug_labs.chapter_08_signal_flow` or launch **Debug Chapter 8 Signal Flow Lab** in VS Code. The lab pauses well around equipment-template creation, graph construction, signal routing, validation, immutable disconnect experiments, visualization generation, and comparison. Inspect `baseline_analysis`, `disconnected_analysis`, `baseline_diagram`, and `comparison` to see how one cable changes the system.

## Chapter 9 Sound Check Debug Lab

Run `python -m open_mic_lab.debug_labs.chapter_09_sound_check` or launch **Debug Chapter 9 Sound Check Lab** in VS Code. Breakpoint markers guide you through venue-profile loading, sound-check workflow construction, mixer analysis, balance calculations, immutable mixer experiments, and comparison of two mixes. Inspect `baseline_analysis`, `workflow`, `raised_monitor`, `monitor_analysis`, `comparison`, `louder_vocal`, `closer_mic`, and `muted_piano` to see why sound check is a decision process rather than a search for one perfect mix.

## Chapter 10 — Audience Experience Debug Lab

Run `python -m open_mic_lab.debug_labs.chapter_10_audience_experience` or use **Debug Chapter 10 Audience Experience Lab** in VS Code. Breakpoints are marked for audience-profile loading, coffeehouse response analysis, church response analysis, comparison without a score, an immutable familiarity experiment, and proof that the source performance remains unchanged.

Useful variables: `profiles`, `performance`, `coffeehouse`, `church`, `coffeehouse_response`, `church_response`, `comparison`, `familiarity_experiment`, `original_unchanged`, and `changed_is_copy`.


## Chapter 11 Recovery Debug Lab

Run `python -m open_mic_lab.debug_labs.chapter_11_recovery` or use **Debug Chapter 11 Recovery Lab** in VS Code. Suggested breakpoints inspect incident creation, recovery analysis, immutable strategy experiments, comparison tradeoffs, and deterministic timeline generation. The helper is designed to show that the report contains educational observations rather than a mistake score.

## Chapter 12 improvisation debug lab

Run:

```bash
python -m open_mic_lab.debug_labs.chapter_12_improvisation
```

Open **Debug Chapter 12 Improvisation Lab** in VS Code. Suggested breakpoints are marked in `src/open_mic_lab/debug_labs/chapter_12_improvisation.py` for opportunity detection, planned timeline generation, immutable experiments, and planned/adapted comparison.
