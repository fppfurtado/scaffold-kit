"""template/cycles/: lean cycle docs aligned with project philosophy."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CYCLE1 = REPO_ROOT / "template" / "cycles" / "cycle-1"


@pytest.mark.parametrize(
    "name",
    ("README.md", "pitch.md", "notes.md", "review.md"),
)
def test_cycle_1_core_files_exist(name: str) -> None:
    path = CYCLE1 / name
    assert path.is_file(), f"missing: {path}"


def test_cycle_readme_documents_three_artifacts() -> None:
    text = (CYCLE1 / "README.md").read_text(encoding="utf-8")
    assert "`pitch.md`" in text
    assert "`notes.md`" in text
    assert "`review.md`" in text
    assert "agente de IA" in text


def test_pitch_is_lean_not_full_prd() -> None:
    text = (CYCLE1 / "pitch.md").read_text(encoding="utf-8")
    assert "No-Gos" in text
    assert "Rabbit holes" in text
    assert "PRD" in text
    assert "YYYY-MM-DD" in text


def test_notes_link_pitch_and_stress_speed() -> None:
    text = (CYCLE1 / "notes.md").read_text(encoding="utf-8")
    assert "`pitch.md`" in text
    assert "agente de IA" in text


def test_review_links_pitch_notes_and_next_steps() -> None:
    text = (CYCLE1 / "review.md").read_text(encoding="utf-8")
    assert "`pitch.md`" in text
    assert "`notes.md`" in text
    assert "spikes/" in text
    assert "YYYY-MM-DD" in text


def test_legacy_xxx_templates_removed() -> None:
    for name in ("PXXX-pitch-template.md", "NXXX-note-template.md", "RXXX-review-template.md"):
        assert not (CYCLE1 / name).is_file(), f"unexpected legacy file: {name}"
