"""Validate per-stack Dockerfile template (template/infra/docker/Dockerfile.jinja)."""

from __future__ import annotations

from pathlib import Path

import pytest
from jinja2 import Environment

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCKERFILE_TEMPLATE_PATH = REPO_ROOT / "template" / "infra" / "docker" / "Dockerfile.jinja"


@pytest.fixture(scope="module")
def dockerfile_template_source() -> str:
    assert DOCKERFILE_TEMPLATE_PATH.is_file(), f"missing template: {DOCKERFILE_TEMPLATE_PATH}"
    return DOCKERFILE_TEMPLATE_PATH.read_text(encoding="utf-8")


def _render(source: str, stack: str) -> str:
    ext = {"python": "py", "typescript": "ts", "go": "go"}[stack]
    return Environment().from_string(source).render(stack=stack, main_extension=ext)


@pytest.mark.parametrize(
    ("stack", "expected_from"),
    [
        ("python", "python:3.12-slim"),
        ("typescript", "node:22-slim"),
        ("go", "golang:1.23"),
    ],
)
def test_from_image_matches_stack(
    dockerfile_template_source: str, stack: str, expected_from: str
) -> None:
    out = _render(dockerfile_template_source, stack)
    assert out.startswith(f"FROM {expected_from}")


def test_no_pip_install_requirements(dockerfile_template_source: str) -> None:
    """Regression: template must not assume requirements.txt for Python."""
    for stack in ("python", "typescript", "go"):
        out = _render(dockerfile_template_source, stack)
        assert "pip install" not in out
        assert "requirements.txt" not in out


def test_python_cmd_uses_main_at_repo_root_src(dockerfile_template_source: str) -> None:
    out = _render(dockerfile_template_source, "python")
    assert 'CMD ["python", "src/main.py"]' in out


def test_typescript_cmd_uses_strip_types_and_main_ts(dockerfile_template_source: str) -> None:
    out = _render(dockerfile_template_source, "typescript")
    assert 'CMD ["node", "--experimental-strip-types", "src/main.ts"]' in out


def test_go_build_and_binary_cmd(dockerfile_template_source: str) -> None:
    out = _render(dockerfile_template_source, "go")
    assert "RUN go build -o /app/bin/main src/main.go" in out
    assert 'CMD ["/app/bin/main"]' in out


def test_regression_no_stack_subdir_main_path(dockerfile_template_source: str) -> None:
    """Would fail if Dockerfile reverted to src/{{ stack | lower }}/main.py."""
    for stack in ("python", "typescript", "go"):
        out = _render(dockerfile_template_source, stack)
        assert "/python/main" not in out
        assert "/typescript/main" not in out
        assert "/go/main" not in out
        assert f"src/{stack}/main" not in out
