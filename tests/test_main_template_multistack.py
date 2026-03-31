"""Validate multi-stack stdlib HTTP main entry template (template/src/main.{{ main_extension }}.jinja)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest
from jinja2 import Environment

REPO_ROOT = Path(__file__).resolve().parents[1]
MAIN_TEMPLATE_PATH = REPO_ROOT / "template" / "src" / "main.{{ main_extension }}.jinja"


@pytest.fixture(scope="module")
def main_template_source() -> str:
    assert MAIN_TEMPLATE_PATH.is_file(), f"missing template: {MAIN_TEMPLATE_PATH}"
    return MAIN_TEMPLATE_PATH.read_text(encoding="utf-8")


def _render(main_template_source: str, stack: str) -> str:
    return Environment().from_string(main_template_source).render(
        stack=stack,
        main_extension={"python": "py", "typescript": "ts", "go": "go"}.get(stack, "py"),
    )


def test_python_stack_uses_stdlib_http_not_fastapi(main_template_source: str) -> None:
    out = _render(main_template_source, "python")
    assert "HTTPServer" in out and "BaseHTTPRequestHandler" in out
    assert "http.server" in out
    assert "fastapi" not in out.lower()


def test_typescript_stack_uses_node_http_create_server(main_template_source: str) -> None:
    out = _render(main_template_source, "typescript")
    assert 'from "node:http"' in out or "from 'node:http'" in out
    assert "createServer" in out
    assert "application/json" in out


def test_go_stack_uses_net_http_listen_and_serve(main_template_source: str) -> None:
    out = _render(main_template_source, "go")
    assert "package main" in out
    assert '"net/http"' in out
    assert "ListenAndServe" in out
    assert "encoding/json" in out


@pytest.mark.parametrize(
    "stack",
    ["python", "typescript", "go"],
)
def test_each_stack_serves_json_status_ok(main_template_source: str, stack: str) -> None:
    out = _render(main_template_source, stack)
    assert "ok" in out
    assert "status" in out


def test_unknown_stack_produces_no_substantive_body(main_template_source: str) -> None:
    """No {% else %}: unsupported stack should not emit application code."""
    out = _render(main_template_source, "rust")
    stripped = out.strip()
    assert stripped == ""


def test_rendered_python_main_is_valid_syntax(main_template_source: str) -> None:
    out = _render(main_template_source, "python")
    ast.parse(out)


def test_regression_fastapi_stub_not_present(main_template_source: str) -> None:
    """Would fail if main template reverted to FastAPI-only."""
    py = _render(main_template_source, "python")
    assert "FastAPI" not in py
