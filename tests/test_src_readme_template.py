"""Validate src README template uses module_name and main_extension (template/src/README.md.tmpl)."""

from __future__ import annotations

from pathlib import Path

import pytest
from jinja2 import Environment

REPO_ROOT = Path(__file__).resolve().parents[1]
README_TEMPLATE_PATH = REPO_ROOT / "template" / "src" / "README.md.tmpl"


@pytest.fixture(scope="module")
def readme_template_source() -> str:
    assert README_TEMPLATE_PATH.is_file(), f"missing template: {README_TEMPLATE_PATH}"
    return README_TEMPLATE_PATH.read_text(encoding="utf-8")


def _render(source: str, *, module_name: str, main_extension: str) -> str:
    return Environment().from_string(source).render(
        module_name=module_name,
        main_extension=main_extension,
    )


def test_regression_no_wrong_jinja_variables(readme_template_source: str) -> None:
    """Would fail if template reverted to {{ extension }} or src/{{ stack }}/."""
    assert "{{ extension }}" not in readme_template_source
    assert "src/{{ stack }}/" not in readme_template_source


def test_uses_module_name_and_main_extension_placeholders(readme_template_source: str) -> None:
    assert "{{ module_name }}" in readme_template_source
    assert "{{ main_extension }}" in readme_template_source


def test_rendered_paths_use_module_and_entry_extension(readme_template_source: str) -> None:
    out = _render(
        readme_template_source,
        module_name="Billing",
        main_extension="py",
    )
    assert "src/Billing/" in out
    assert "`main.py`" in out
