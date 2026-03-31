"""Validate per-stack GitHub Actions CI template (template/.github/workflows/ci.yaml.jinja)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from jinja2 import Environment

REPO_ROOT = Path(__file__).resolve().parents[1]
CI_TEMPLATE_PATH = REPO_ROOT / "template" / ".github" / "workflows" / "ci.yaml.jinja"


@pytest.fixture(scope="module")
def ci_template_source() -> str:
    assert CI_TEMPLATE_PATH.is_file(), f"missing template: {CI_TEMPLATE_PATH}"
    return CI_TEMPLATE_PATH.read_text(encoding="utf-8")


def _render(source: str, stack: str) -> str:
    return Environment().from_string(source).render(stack=stack)


def _parsed_workflow(rendered: str) -> dict:
    return yaml.safe_load(rendered)


def test_python_includes_setup_python(ci_template_source: str) -> None:
    out = _render(ci_template_source, "python")
    doc = _parsed_workflow(out)
    steps = doc["jobs"]["test"]["steps"]
    assert {"uses": "actions/checkout@v4"} in steps
    assert {
        "uses": "actions/setup-python@v5",
        "with": {"python-version": "3.12"},
    } in steps
    assert {"run": "make test"} in steps
    assert "setup-node" not in out
    assert "setup-go" not in out


def test_typescript_includes_setup_node(ci_template_source: str) -> None:
    out = _render(ci_template_source, "typescript")
    doc = _parsed_workflow(out)
    steps = doc["jobs"]["test"]["steps"]
    assert {"uses": "actions/checkout@v4"} in steps
    assert {
        "uses": "actions/setup-node@v4",
        "with": {"node-version": "22"},
    } in steps
    assert {"run": "make test"} in steps
    assert "setup-python" not in out
    assert "setup-go" not in out


def test_go_includes_setup_go(ci_template_source: str) -> None:
    out = _render(ci_template_source, "go")
    doc = _parsed_workflow(out)
    steps = doc["jobs"]["test"]["steps"]
    assert {"uses": "actions/checkout@v4"} in steps
    assert {
        "uses": "actions/setup-go@v5",
        "with": {"go-version": "1.23"},
    } in steps
    assert {"run": "make test"} in steps
    assert "setup-python" not in out
    assert "setup-node" not in out


def test_regression_no_placeholder_setup_step(ci_template_source: str) -> None:
    """Would fail if workflow reverted to a single generic 'Setup {{ stack }}' stub."""
    src = ci_template_source
    assert "Setup {{ stack }}" not in src
    assert "# ... (configuração simples)" not in src


@pytest.mark.parametrize("stack", ["python", "typescript", "go"])
def test_workflow_is_valid_yaml_for_each_stack(ci_template_source: str, stack: str) -> None:
    out = _render(ci_template_source, stack)
    doc = _parsed_workflow(out)
    assert doc["name"] == "CI"
    assert doc["jobs"]["test"]["runs-on"] == "ubuntu-latest"
