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
