# Research: Task CLI (atomic writes, ID assignment, concurrency)

**Decision**: Use stdlib-based atomic write pattern: write JSON to a temporary file in the same directory, call `os.fsync()` on the file descriptor, then `os.replace()` to atomically replace the target file.

**Rationale**: This pattern avoids partial writes and is cross-platform for Python 3.8+. It avoids introducing dependency on external libraries and is simple to test via simulated crashes in integration tests.

**Alternatives considered**:
- File locks (fcntl / portalocker): provides stronger concurrency guarantees but increases complexity and external dependency risk, and can be platform-specific.
- SQLite: robust transactional storage, but violates the "minimal dependencies / simplicity" principle.

**Decision**: Implement atomic writes as above and document cooperative concurrency assumptions (single-user CLI). If future needs require concurrent safe multi-writer support, migrate to a lock-based approach or SQLite.

## ID assignment

**Decision**: `id` assignment uses `max(existing_ids) + 1` when adding a new task. If the file is empty, ids start at 1. If the file is malformed, attempts to recover will raise an error and the CLI will return a non-zero exit code; repair instructions will be provided in quickstart.md.

**Rationale**: Deterministic, simple, and testable. Avoids maintaining separate sequence files.

## CLI parsing choice

**Decision**: Use `argparse` from stdlib for the MVP CLI. Keep the CLI thin and delegate logic to library functions.

**Rationale**: No external dependency, adequate for the required command set, easy to test.
