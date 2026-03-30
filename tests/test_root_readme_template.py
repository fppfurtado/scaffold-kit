"""Validate root README template has project title and description (template/README.md.tmpl)."""

from __future__ import annotations

from pathlib import Path

import pytest
from jinja2 import Environment

REPO_ROOT = Path(__file__).resolve().parents[1]
README_TEMPLATE_PATH = REPO_ROOT / "template" / "README.md.tmpl"


@pytest.fixture(scope="module")
def readme_template_source() -> str:
    assert README_TEMPLATE_PATH.is_file(), f"missing template: {README_TEMPLATE_PATH}"
    return README_TEMPLATE_PATH.read_text(encoding="utf-8")


def _render(source: str, *, project_name: str, description: str) -> str:
    return Environment().from_string(source).render(
        project_name=project_name,
        description=description,
    )


def test_has_project_name_and_description_placeholders(readme_template_source: str) -> None:
    assert "# {{ project_name }}" in readme_template_source
    assert "{{ description }}" in readme_template_source


def test_rendered_readme_starts_with_title_and_description(readme_template_source: str) -> None:
    out = _render(
        readme_template_source,
        project_name="acme-api",
        description="Serviço interno de integração.",
    )
    lines = out.splitlines()
    assert lines[0] == "# acme-api"
    assert lines[1] == ""
    assert lines[2] == "Serviço interno de integração."
    assert lines[3] == ""


def test_regression_title_block_not_removed(readme_template_source: str) -> None:
    """Would fail if header reverted to starting at ## Estrutura."""
    stripped = readme_template_source.lstrip()
    assert stripped.startswith("# {{ project_name }}")
