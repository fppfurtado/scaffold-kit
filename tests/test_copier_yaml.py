"""Validate template/copier.yaml header comment and module_name help (plan 2.1)."""

from __future__ import annotations

from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
COPIER_YAML_PATH = REPO_ROOT / "template" / "copier.yaml"


def test_first_line_comment_names_copier_yaml() -> None:
    """Regression: header must say copier.yaml, not copier.yml."""
    first_line = COPIER_YAML_PATH.read_text(encoding="utf-8").splitlines()[0]
    assert first_line == "# copier.yaml"


def test_module_name_help_is_stack_neutral() -> None:
    """module_name applies to python, typescript, and go; help must not say Python-only."""
    data = yaml.safe_load(COPIER_YAML_PATH.read_text(encoding="utf-8"))
    assert data["module_name"]["help"] == (
        "Nome do módulo principal para imports e estrutura interna"
    )
    assert "Python" not in data["module_name"]["help"]
