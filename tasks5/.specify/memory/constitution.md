<!--
Sync Impact Report

- Version change: none -> 1.0.0
- Modified principles: (added) "I. Library + CLI Separation"; "II. Simple Data Model"; "III. File-backed JSON Persistence"; "IV. Test-First & Deterministic Behavior"; "V. Minimal Dependencies & Simplicity"
- Added sections: "Additional Constraints", "Development Workflow"
- Removed sections: none
- Templates requiring updates: /Users/shan/Downloads/tasks5-spec-kit/.specify/templates/plan-template.md ✅ updated
	/Users/shan/Downloads/tasks5-spec-kit/.specify/templates/spec-template.md ⚠ pending
	/Users/shan/Downloads/tasks5-spec-kit/.specify/templates/tasks-template.md ⚠ pending
	/Users/shan/Downloads/tasks5-spec-kit/.specify/templates/checklist-template.md ⚠ pending
	/Users/shan/Downloads/tasks5-spec-kit/.specify/templates/agent-file-template.md ⚠ pending
- Follow-up TODOs: none (no remaining bracketed placeholders)
-->

# Task CLI Constitution

## Core Principles

### I. Library + CLI Separation
Core logic MUST be implemented as importable, well-documented Python modules (the "library"). The CLI MUST be a thin adapter that only handles argument parsing, invocation of library functions, and user-facing I/O. Rationale: keeps business logic testable, reusable, and independent from the interface.

### II. Simple Data Model (Task)
The system MUST represent tasks with an explicit, simple schema: `id` (integer), `description` (string), `completed` (boolean). The schema is authoritative for storage and tests. Rationale: an explicit minimal data model reduces ambiguity, simplifies migrations, and ensures interoperability across tools.

### III. File-backed JSON Persistence
Persistent storage MUST be a single JSON file on disk (default: `tasks.json` in the project or user config directory). Writes MUST be atomic (write temp → fsync → rename) to avoid corruption. The project MUST document the storage path and provide a configurable override. Rationale: predictable, human-readable persistence with minimal operational requirements.

### IV. Test-First & Deterministic Behavior
Behavioral requirements and edge cases MUST be expressed as automated tests (unit + small integration tests). Tests describing user stories MUST be written before or alongside implementation and MUST be runnable with `pytest`. Deterministic behavior (e.g., ID assignment, ordering) MUST be specified and covered by tests. Rationale: ensures correctness, avoids regressions, and documents expected behavior.

### V. Minimal Dependencies & Simplicity
The project MUST minimize external dependencies and prefer stdlib solutions where reasonable. Any third-party dependency MUST have explicit justification in the plan. The CLI UX MUST be simple and composable (clear commands: `add`, `list`, `done`). Rationale: reduces maintenance burden and simplifies installation for end users.

## Additional Constraints

- Language/Version: Python 3.11+ recommended.
- Storage: file-backed JSON (see Principle III). Concurrency is cooperative; the project MUST document assumptions (single-user CLI vs. concurrent access).
- Testing: `pytest` for unit/integration tests; tests MUST be in `tests/` with clear separation (unit/integration).
- Target Platform: POSIX-compatible shells (tested with `zsh`, `bash`) and cross-platform where feasible.

## Development Workflow

- PRs MUST include tests for new behaviors and pass CI checks before merging.
- Code review MUST validate adherence to the constitution's principles (library/CLI separation, persistence rules, minimal deps).
- The `plan.md`/`spec.md`/`tasks.md` workflow outlined in `.specify/templates/` MUST be followed for new features.

## Governance

- Amendments: Proposals to change this constitution MUST be captured as a spec and reviewed in a PR. Minor wording/clarity changes are PATCH bumps; new principles or material expansions are MINOR bumps; removals or backward-incompatible changes are MAJOR bumps.
- Versioning policy: Use semantic versioning for the constitution itself (`MAJOR.MINOR.PATCH`). Bump rules:
	- MAJOR: Backward incompatible governance/principle removals or redefinitions.
	- MINOR: New principle/section added or materially expanded guidance.
	- PATCH: Clarifications, wording, typo fixes, non-semantic refinements.
- Compliance review: Each release/merge MUST state conformity in the PR description and reference any exceptions with justifications.

**Version**: 1.0.0 | **Ratified**: 2025-11-19 | **Last Amended**: 2025-11-19

