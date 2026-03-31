"""Validate docker-compose template (template/docker-compose.yml.jinja)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from jinja2 import Environment

REPO_ROOT = Path(__file__).resolve().parents[1]
COMPOSE_TEMPLATE_PATH = REPO_ROOT / "template" / "docker-compose.yml.jinja"


@pytest.fixture(scope="module")
def compose_template_source() -> str:
    assert COMPOSE_TEMPLATE_PATH.is_file(), f"missing template: {COMPOSE_TEMPLATE_PATH}"
    return COMPOSE_TEMPLATE_PATH.read_text(encoding="utf-8")


def _render(source: str) -> str:
    return Environment().from_string(source).render()


def test_compose_template_renders_valid_yaml(compose_template_source: str) -> None:
    rendered = _render(compose_template_source)
    data = yaml.safe_load(rendered)
    assert isinstance(data, dict)
    assert "services" in data
    assert "app" in data["services"]


def test_compose_build_points_at_infra_dockerfile(compose_template_source: str) -> None:
    rendered = _render(compose_template_source)
    data = yaml.safe_load(rendered)
    build = data["services"]["app"]["build"]
    assert build["context"] == "."
    assert build["dockerfile"] == "infra/docker/Dockerfile"


def test_compose_exposes_port_8000(compose_template_source: str) -> None:
    rendered = _render(compose_template_source)
    data = yaml.safe_load(rendered)
    ports = data["services"]["app"]["ports"]
    assert "8000:8000" in ports


def test_compose_uses_env_file(compose_template_source: str) -> None:
    rendered = _render(compose_template_source)
    data = yaml.safe_load(rendered)
    assert data["services"]["app"]["env_file"] == [".env"]
