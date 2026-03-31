"""Validate stack-aware Makefile template (template/Makefile.tmpl)."""

from __future__ import annotations

from pathlib import Path

import pytest
from jinja2 import Environment

REPO_ROOT = Path(__file__).resolve().parents[1]
MAKEFILE_TEMPLATE_PATH = REPO_ROOT / "template" / "Makefile.tmpl"


@pytest.fixture(scope="module")
def makefile_template_source() -> str:
    assert MAKEFILE_TEMPLATE_PATH.is_file(), f"missing template: {MAKEFILE_TEMPLATE_PATH}"
    return MAKEFILE_TEMPLATE_PATH.read_text(encoding="utf-8")


def _render(source: str, stack: str) -> str:
    return Environment().from_string(source).render(stack=stack)


def test_python_dev_test_clean(makefile_template_source: str) -> None:
    out = _render(makefile_template_source, "python")
    assert "\ndev:\n\tpython src/main.py\n" in out
    assert "python -m pytest tests/" in out
    assert "__pycache__" in out and ".pytest_cache" in out
    assert "npx vitest" not in out
    assert "go run" not in out


def test_typescript_dev_test_clean(makefile_template_source: str) -> None:
    out = _render(makefile_template_source, "typescript")
    assert "node --experimental-strip-types src/main.ts" in out
    assert "npx vitest run" in out
    assert "node_modules" in out and ".cache" in out
    assert "pytest" not in out
    assert "go test" not in out


def test_go_dev_test_clean(makefile_template_source: str) -> None:
    out = _render(makefile_template_source, "go")
    assert "go run src/main.go" in out
    assert "go test ./..." in out
    assert "bin/" in out and "vendor/" in out
    assert "pytest" not in out
    assert "vitest" not in out


@pytest.mark.parametrize("stack", ["python", "typescript", "go"])
def test_up_target_docker_compose_all_stacks(
    makefile_template_source: str, stack: str
) -> None:
    out = _render(makefile_template_source, stack)
    assert "up:\n\tdocker compose up --build" in out


def test_no_blank_line_between_target_and_recipe_python(
    makefile_template_source: str,
) -> None:
    """Blank line after 'dev:' ends the recipe in GNU make; keep target contiguous."""
    out = _render(makefile_template_source, "python")
    assert "dev:\n\n\t" not in out


def test_regression_not_placeholder_comments(makefile_template_source: str) -> None:
    """Would fail if Makefile reverted to stack-agnostic placeholders."""
    src = makefile_template_source
    assert "Adicione aqui o comando" not in src
    assert "# pytest ou vitest" not in src
