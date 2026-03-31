"""template/cycles/: lean cycle docs aligned with project philosophy (P/N/R + XXX convention)."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CYCLE1 = REPO_ROOT / "template" / "cycles" / "cycle-1"


@pytest.mark.parametrize(
    "name",
    (
        "README.md",
        "PXXX-pitch-template.md",
        "NXXX-note-template.md",
        "RXXX-review-template.md",
    ),
)
def test_cycle_1_core_files_exist(name: str) -> None:
    path = CYCLE1 / name
    assert path.is_file(), f"missing: {path}"


def test_cycle_readme_documents_p_n_r_templates() -> None:
    text = (CYCLE1 / "README.md").read_text(encoding="utf-8")
    assert "`PXXX-pitch-template.md`" in text
    assert "`NXXX-note-template.md`" in text
    assert "`RXXX-review-template.md`" in text
    assert "discovery/" in text
    assert "agente de IA" in text


def test_pitch_template_is_lean_not_full_prd() -> None:
    text = (CYCLE1 / "PXXX-pitch-template.md").read_text(encoding="utf-8")
    assert "No-Gos" in text
    assert "Rabbit holes" in text
    assert "PRD" in text
    assert "YYYY-MM-DD" in text


def test_note_template_links_pitch_convention() -> None:
    text = (CYCLE1 / "NXXX-note-template.md").read_text(encoding="utf-8")
    assert "PXXX-pitch-template.md" in text
    assert "agente de IA" in text


def test_review_template_links_p_and_n_conventions() -> None:
    text = (CYCLE1 / "RXXX-review-template.md").read_text(encoding="utf-8")
    assert "PXXX-pitch-template.md" in text
    assert "NXXX-note-template.md" in text
    assert "spikes/" in text
    assert "YYYY-MM-DD" in text


def test_legacy_short_names_removed() -> None:
    for name in ("pitch.md", "notes.md", "review.md"):
        assert not (CYCLE1 / name).is_file(), f"unexpected short-name file: {name}"
