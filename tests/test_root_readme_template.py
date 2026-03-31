"""Validate root README template (template/README.md.tmpl)."""

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


def _render(source: str, **context: object) -> str:
    defaults: dict[str, object] = {
        "project_name": "acme-api",
        "description": "Serviço interno de integração.",
        "stack": "python",
        "main_extension": "py",
        "module_name": "acme_api",
        "include_domain_model": True,
        "use_clean_architecture": True,
    }
    defaults.update(context)
    return Environment().from_string(source).render(**defaults)


def test_has_project_name_and_description_placeholders(readme_template_source: str) -> None:
    assert "# {{ project_name }}" in readme_template_source
    assert "{{ description }}" in readme_template_source


def test_rendered_readme_starts_with_title_and_description(readme_template_source: str) -> None:
    out = _render(readme_template_source)
    lines = out.splitlines()
    assert lines[0] == "# acme-api"
    assert lines[1] == ""
    assert lines[2] == "Serviço interno de integração."
    assert lines[3] == ""
    assert lines[4] == "## Stack"


def test_regression_title_block_not_removed(readme_template_source: str) -> None:
    """Would fail if header reverted to starting at ## Estrutura."""
    stripped = readme_template_source.lstrip()
    assert stripped.startswith("# {{ project_name }}")


def test_render_includes_stack_main_and_compose(readme_template_source: str) -> None:
    out = _render(readme_template_source)
    assert "**python**" in out or "stack **python**" in out
    assert "`src/main.py`" in out
    assert "docker-compose.yml" in out
    assert ".editorconfig" in out
    assert ".env.example" in out
    assert "cycles/cycle-1/" in out
    assert "pitch.md" in out


def test_render_typescript_stack_uses_main_ts(readme_template_source: str) -> None:
    out = _render(readme_template_source, stack="typescript", main_extension="ts")
    assert "**typescript**" in out
    assert "`src/main.ts`" in out


def test_render_without_domain_omits_domain_doc_and_steps(readme_template_source: str) -> None:
    out = _render(readme_template_source, include_domain_model=False)
    assert "**`domain.md`**" not in out
    assert "docs/domain.md" not in out
    assert "**Domain**" not in out


def test_render_without_clean_architecture_skips_layer_list(readme_template_source: str) -> None:
    out = _render(readme_template_source, use_clean_architecture=False)
    assert "Estrutura sugerida em camadas" not in out
    assert "Casos de uso e orquestração" not in out
    assert "- `app/`" not in out
    assert "src/acme_api/spikes/" in out
