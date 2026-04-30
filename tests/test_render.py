"""Smoke tests for scaffold-kit v2 render.

Renders the template into a tmp dir with both `use_docker=true` and `use_docker=false`,
asserts the resulting structure matches the documented spec.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
COPIER_YAML = REPO_ROOT / "template" / "copier.yaml"

ANSWERS_BASE = {
    "project_name": "Demo Project",
    "project_slug": "demo-project",
    "module_name": "demo_project",
    "description": "Demo project for render smoke test",
}


def _render(tmp_path: Path, use_docker: bool) -> Path:
    out = tmp_path / "render"
    answers = {**ANSWERS_BASE, "use_docker": use_docker}
    cmd = [
        "copier",
        "copy",
        "--defaults",
        "--trust",
        "--vcs-ref=HEAD",
    ]
    for key, value in answers.items():
        cmd.extend(["--data", f"{key}={value}"])
    cmd.extend([str(REPO_ROOT / "template"), str(out)])
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"copier failed:\n{result.stdout}\n{result.stderr}"
    return out


def test_copier_yaml_has_expected_questions() -> None:
    data = yaml.safe_load(COPIER_YAML.read_text(encoding="utf-8"))
    questions = {k for k, v in data.items() if not k.startswith("_") and isinstance(v, dict)}
    assert questions == {
        "project_name",
        "project_slug",
        "module_name",
        "description",
        "use_docker",
    }


def test_render_with_docker_creates_docker_files(tmp_path: Path) -> None:
    out = _render(tmp_path, use_docker=True)
    assert (out / "docker-compose.yml").is_file()
    assert (out / ".dockerignore").is_file()
    assert (out / "infra" / "docker" / "Dockerfile").is_file()


def test_render_without_docker_omits_docker_files(tmp_path: Path) -> None:
    out = _render(tmp_path, use_docker=False)
    assert not (out / "docker-compose.yml").exists()
    assert not (out / ".dockerignore").exists()
    assert not (out / "infra").exists()


@pytest.mark.parametrize("use_docker", [True, False])
def test_render_always_creates_core_structure(tmp_path: Path, use_docker: bool) -> None:
    out = _render(tmp_path, use_docker=use_docker)
    expected = [
        "CLAUDE.md",
        "IDEA.md",
        "README.md",
        "BACKLOG.md",
        "Makefile",
        "pyproject.toml",
        ".editorconfig",
        ".gitignore",
        ".env.example",
        ".worktreeinclude",
        "docs/domain.md",
        "docs/design.md",
        "docs/decisions/ADR-template.md",
        f"src/demo_project/__init__.py",
        f"src/demo_project/main.py",
        "tests/conftest.py",
        ".github/workflows/ci.yml",
    ]
    missing = [p for p in expected if not (out / p).exists()]
    assert not missing, f"missing files: {missing}"


def test_rendered_idea_uses_project_name(tmp_path: Path) -> None:
    out = _render(tmp_path, use_docker=True)
    idea = (out / "IDEA.md").read_text(encoding="utf-8")
    assert "# IDEA — Demo Project" in idea
    assert "Demo project for render smoke test" in idea


def test_rendered_pyproject_uses_module_name(tmp_path: Path) -> None:
    out = _render(tmp_path, use_docker=True)
    pyproject = (out / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "demo-project"' in pyproject
