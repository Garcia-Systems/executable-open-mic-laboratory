# Research Audit Plan

This planning document was created before modifying repository content for the research-foundation milestone.

## Inspection scope

The audit covers all Volume I chapters (`docs/chapters/chapter-00` through `chapter-15`), repository documentation, CLI demonstrations, debug laboratories, domain models, and service/scoring engines under `src/open_mic_lab/services`.

## Initial findings

- The repository already uses transparent deterministic formulas and educational disclaimers, but citations are sparse and not centralized.
- Chapters explain learner-facing concepts clearly, yet they rarely distinguish established research, professional practice, engineering standards, repository heuristics, and subjective artistic judgment.
- Scoring engines are documented as educational tools in code comments and README language, but not consistently with a shared evidence vocabulary.
- Audio chapters would benefit from professional audio references and an explicit separation between engineering principles and venue-specific practice.
- Practice, reflection, feedback, coordination, and simulation chapters would benefit from stronger links to educational psychology, deliberate practice, self-regulated learning, cognitive load, metacognition, and simulation-based learning.
- Stage presence, audience experience, original music, and repertoire-fit chapters should identify where empirical literature motivates attention to audience perception while preserving room for subjective artistic choice.

## Modification plan

1. Create a centralized APA-style bibliography in `docs/references.md`.
2. Create `docs/research-foundations.md` to define evidence categories, limitations, and the repository's educational modeling stance.
3. Create `docs/source-map.md` to map research areas to services, chapters, CLIs, and debug labs.
4. Create `docs/research-guidelines.md` for future contributors.
5. Add concise Research Foundations and References and Further Reading sections to every chapter.
6. Update README and architecture documentation to describe evidence-informed deterministic simulation.
7. Add reusable scoring-engine documentation to services without changing deterministic behavior.
8. Run pytest, Ruff, formatting checks, and mypy.

## Audit principle

The milestone will not claim that literature validates exact repository scores. It will state that research and professional practice motivate educational concepts, while the deterministic formulas are repository-designed learning heuristics.
