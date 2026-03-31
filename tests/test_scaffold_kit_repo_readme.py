"""Sanity checks for repository root README.md (accurate structure and no stray Jinja)."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
README_PATH = REPO_ROOT / "README.md"


@pytest.fixture(scope="module")
def readme_text() -> str:
    assert README_PATH.is_file(), f"missing: {README_PATH}"
    return README_PATH.read_text(encoding="utf-8")


def test_repo_readme_exists() -> None:
    assert README_PATH.is_file()


def test_repo_readme_has_no_literal_jinja_placeholders(readme_text: str) -> None:
    """Root README documents the kit; literal {{ }} would read like broken template output."""
    assert "{{" not in readme_text
    assert "{%" not in readme_text


def test_repo_readme_documents_stacks_and_entrypoint(readme_text: str) -> None:
    for needle in ("Python", "TypeScript", "Go", "src/main."):
        assert needle in readme_text


def test_repo_readme_structure_matches_template_layout(readme_text: str) -> None:
    assert "docs/strategy/spikes/" in readme_text
    assert "docker-compose.yml" in readme_text
    assert ".tmpl" in readme_text
