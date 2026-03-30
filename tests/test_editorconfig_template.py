"""Validate EditorConfig in template (template/.editorconfig)."""

from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
EDITORCONFIG_PATH = REPO_ROOT / "template" / ".editorconfig"


@pytest.fixture(scope="module")
def editorconfig_text() -> str:
    assert EDITORCONFIG_PATH.is_file(), f"missing template file: {EDITORCONFIG_PATH}"
    return EDITORCONFIG_PATH.read_text(encoding="utf-8")


def test_editorconfig_exists() -> None:
    assert EDITORCONFIG_PATH.is_file()


def test_editorconfig_root_and_global_section(editorconfig_text: str) -> None:
    assert "root = true" in editorconfig_text
    assert "[*]" in editorconfig_text
    assert "end_of_line = lf" in editorconfig_text
    assert "insert_final_newline = true" in editorconfig_text
    assert "charset = utf-8" in editorconfig_text
    assert "indent_style = space" in editorconfig_text
    assert "indent_size = 2" in editorconfig_text


def test_editorconfig_python_and_makefile_sections(editorconfig_text: str) -> None:
    assert "[*.py]" in editorconfig_text
    assert "indent_size = 4" in editorconfig_text
    assert "[Makefile]" in editorconfig_text
    assert "indent_style = tab" in editorconfig_text
