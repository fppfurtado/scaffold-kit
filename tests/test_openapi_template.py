"""Validate generic OpenAPI contract template (contracts/openapi.yaml.tmpl)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from jinja2 import Environment

REPO_ROOT = Path(__file__).resolve().parents[1]
OPENAPI_TEMPLATE_PATH = (
    REPO_ROOT
    / "template"
    / "src"
    / "{{ module_name | lower }}"
    / "{% if use_clean_architecture %}interfaces{% endif %}"
    / "contracts"
    / "openapi.yaml.tmpl"
)


@pytest.fixture(scope="module")
def openapi_template_source() -> str:
    assert OPENAPI_TEMPLATE_PATH.is_file(), f"missing template: {OPENAPI_TEMPLATE_PATH}"
    return OPENAPI_TEMPLATE_PATH.read_text(encoding="utf-8")


def _render(source: str) -> str:
    return Environment().from_string(source).render(
        project_name="acme-service",
        domain="example",
    )


def test_rendered_yaml_parses(openapi_template_source: str) -> None:
    out = _render(openapi_template_source)
    data = yaml.safe_load(out)
    assert data["openapi"] == "3.1.0"
    assert "paths" in data


def test_items_crud_paths_and_schemas(openapi_template_source: str) -> None:
    out = _render(openapi_template_source)
    data = yaml.safe_load(out)
    paths = data["paths"]
    assert "/health" in paths
    assert "/items" in paths
    assert "/items/{itemId}" in paths
    assert "get" in paths["/items"]
    assert "post" in paths["/items"]
    assert "get" in paths["/items/{itemId}"]
    assert "patch" in paths["/items/{itemId}"]
    assert "delete" in paths["/items/{itemId}"]
    schemas = data["components"]["schemas"]
    assert "CreateItemRequest" in schemas
    assert "ItemResponse" in schemas
    assert "ErrorResponse" in schemas
    assert "HealthResponse" in schemas


def test_regression_no_conciliacao_contract(openapi_template_source: str) -> None:
    """Would fail if template reverted to /agents/conciliar or conciliation schemas."""
    text = openapi_template_source.lower()
    assert "conciliar" not in text
    assert "concilia" not in text
    assert "/agents/" not in text
    assert "concili" not in text
    rendered = _render(openapi_template_source).lower()
    assert "conciliar" not in rendered
    assert "concili" not in rendered


def test_project_name_rendered_in_info(openapi_template_source: str) -> None:
    out = _render(openapi_template_source)
    data = yaml.safe_load(out)
    assert data["info"]["title"] == "Acme-Service API"
    assert "acme-service" in data["info"]["description"]
