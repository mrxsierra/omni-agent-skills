---
name: pytest-verification-runner
description: Authors and executes unit, integration, and property-based verification test suites using Pytest and unittest to empirically catch regressions and validate invariants.
---

# 🧪 Pytest Verification Runner

The **Pytest Verification Runner** authors and executes verification test suites, validates boundary conditions, and ensures all code modifications pass empirical checks before commit or merge.

## 1. Inputs & Context Required
- **Target Source Code:** Implementation modules, functions, or classes under test.
- **Specification & Invariants:** Expected behaviors, return types, exception conditions, and contract boundaries.
- **Test Environment:** Test runner framework (`pytest` or Python standard library `unittest`) and required fixtures.

## 2. Step-by-Step Procedure
1. **Define Failing Invariants First:** Author targeted test cases asserting expected inputs and boundary conditions before making complex implementation changes.
2. **Fixture & Mock Scoping:** Use scoped test fixtures for database handles, file operations (e.g. `tempfile.TemporaryDirectory()`), and HTTP mocks to prevent cross-test pollution.
3. **Preserve Assertions:** Never delete failing tests, disable assertions, or comment out checks to simulate a passing build. If a test fails, diagnose the underlying failure contract.
4. **Execute Verification Command:** Run the test discovery suite (`python3 -m unittest discover -s tests -p 'test_*.py'` or `pytest`) in the terminal and report actual test counts and execution times.

## 3. Expected Outputs & Artifacts
- **Test File:** Cleanly structured test file under `tests/test_<module>.py` containing descriptive test methods.
- **Execution Log:** Verifiable test output reporting test counts, execution duration, and pass status.

## 4. Constraints & Tool Neutrality
- **Framework Compatibility:** Written for Python test suites (`unittest` or `pytest`), adaptable to other test runners.
- **Non-Destructive:** Test runs must clean up temporary directories and avoid mutating persistent workspace files.
