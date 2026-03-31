"""Regression: strategy/domain doc templates must reference module_name paths, not stack."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

DOC_TEMPLATES = [
    REPO_ROOT
    / "template"
    / "docs"
    / "{% if include_domain_model %}domain.md.tmpl{% endif %}",
    REPO_ROOT / "template" / "docs" / "strategy" / "spikes" / "README.md.tmpl",
    REPO_ROOT
    / "template"
    / "docs"
    / "strategy"
    / "spikes"
    / "SXXX-spike-template.md.tmpl",
    REPO_ROOT
    / "template"
    / "src"
    / "{{ module_name | lower }}"
    / "spikes"
    / "README.md.tmpl",
]


@pytest.mark.parametrize("path", DOC_TEMPLATES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_doc_templates_do_not_use_stack_in_src_paths(path: Path) -> None:
    """Would fail if docs reverted to src/{{ stack }}/ (wrong Copier variable for package path)."""
    assert path.is_file(), f"missing template: {path}"
    text = path.read_text(encoding="utf-8")
    assert "src/{{ stack }}/" not in text


@pytest.mark.parametrize("path", DOC_TEMPLATES, ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_doc_templates_use_module_name_in_src_paths(path: Path) -> None:
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "src/{{ module_name }}/" in text


def test_pitches_readme_references_cycle_1_pitch_template() -> None:
    """Pitches README must point at cycles/cycle-1/PXXX-pitch-template.md (same naming convention as docs)."""
    path = REPO_ROOT / "template" / "docs" / "strategy" / "pitches" / "README.md"
    assert path.is_file(), f"missing: {path}"
    text = path.read_text(encoding="utf-8")
    assert "cycles/cycle-1/PXXX-pitch-template.md" in text
    assert "cycles/cycle-01/pitch.md" not in text
