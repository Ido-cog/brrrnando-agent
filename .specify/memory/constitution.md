# Brrrnardo Project Constitution

## Core Principles

### I. Spec-First Architecture
Every feature begins with a detailed update to `SPEC.md`. No code is written until the specification is defined, reviewed, and approved. The Spec is the single source of truth; if the code contradicts the Spec, the code is wrong.

### II. Test-Driven Development (TDD)
Tests must be written before implementation logic.
1. Write a failing test based on the Spec.
2. Verify it fails.
3. Write the minimum code to pass.
4. Refactor.

### III. Atomic Modularity
Code must be organized into loosely coupled, highly cohesive modules. Each module should have a clear public interface and hidden implementation details. Avoid circular dependencies.

### IV. Documentation Parity
Documentation updates are treated with the same rigor as code updates. If the code changes, the documentation (including inline comments and external docs) must be updated in the same commit.

### V. AI Verification
All AI-generated code must be manually reviewed for security, performance, and adherence to these principles. "It works" is not sufficient; it must be correct, maintainable, and understood by the human reviewer.

## Operational Standards

### Code Style & Quality
- Follow the language-specific style guides defined in `.editorconfig` and linter settings.
- Comments should explain *why*, not *what*.
- Functions should be small and do one thing well.

### Git Workflow
- Feature branches named `feat/description` or `fix/issue-id`.
- Commit messages must reference the relevant Spec section or Issue ID.
- Squashed commits preferred for cleaner history upon merge.

## Governance

This Constitution supersedes individual preferences. Amendments require a Pull Request with a clear rationale and team consensus. All PRs must verify compliance with these principles before merging.

**Version**: 1.0.0 
