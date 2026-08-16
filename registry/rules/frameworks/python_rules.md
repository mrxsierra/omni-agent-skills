---
trigger: model_decision
description: Python, FastAPI, and Data Science Coding Standards & Rules.
---

# 🐍 Python & Data Science Standards

These rules apply when writing, editing, or auditing Python scripts, FastAPI/Flask services, and data processing pipelines.

## 1. Code Quality & Type Safety
- **Type Annotations:** Use explicit type hints (`str`, `int`, `List[T]`, `Optional[T]`) for all public function signatures.
- **Docstrings & Comments:** Preserve docstrings and comments. Use Google or Sphinx docstring format for public API modules.
- **Error Handling:** Avoid bare `except:` clauses. Catch specific exceptions (`ValueError`, `FileNotFoundError`, `KeyError`) and preserve stack trace context using `raise ... from err`.

## 2. Testing & Verification (Pytest)
- **Pytest Conventions:** Place test files in `tests/` directory with `test_*.py` naming convention.
- **Fixtures:** Use `pytest` fixtures for database connections, HTTP client mocks, and temporary file paths.
