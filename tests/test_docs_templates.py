"""Docs under template/docs/: content aligned with project philosophy and Jinja where applicable."""

from __future__ import annotations

from pathlib import Path

import pytest
from jinja2 import Environment

REPO_ROOT = Path(__file__).resolve().parents[1]
DISCOVERY = REPO_ROOT / "template" / "docs" / "strategy" / "discovery" / "DXXX-discovery-template.md"
SPIKES_README_TMPL = REPO_ROOT / "template" / "docs" / "strategy" / "spikes" / "README.md.tmpl"
SPIKE_TEMPLATE_TMPL = REPO_ROOT / "template" / "docs" / "strategy" / "spikes" / "SXXX-spike-template.md.tmpl"
ADR_TEMPLATE = REPO_ROOT / "template" / "docs" / "architecture" / "adrs" / "ADR-XXX-template.md"
ADRS_README = REPO_ROOT / "template" / "docs" / "architecture" / "adrs" / "README.md"


def test_discovery_template_stresses_lightweight_capture() -> None:
    text = DISCOVERY.read_text(encoding="utf-8")
    assert "## Problema" in text
    assert "PRD" in text
    assert "agentes de IA" in text


def test_spikes_readme_template_conditional_domain_block() -> None:
    src = SPIKES_README_TMPL.read_text(encoding="utf-8")
    assert "{% if include_domain_model %}" in src
    assert "docs/domain.md" in src


def test_spikes_readme_renders_with_and_without_domain_model() -> None:
    env = Environment()
    rendered_true = env.from_string(SPIKES_README_TMPL.read_text(encoding="utf-8")).render(
        include_domain_model=True,
        module_name="acme_api",
    )
    rendered_false = env.from_string(SPIKES_README_TMPL.read_text(encoding="utf-8")).render(
        include_domain_model=False,
        module_name="acme_api",
    )
    assert "docs/domain.md" in rendered_true
    assert "docs/domain.md" not in rendered_false
    assert "discovery" in rendered_false


def test_spike_sxxx_template_renders_and_keeps_module_paths() -> None:
    src = SPIKE_TEMPLATE_TMPL.read_text(encoding="utf-8")
    assert "src/{{ module_name }}/spikes/" in src
    out = Environment().from_string(src).render(module_name="acme_api")
    assert "src/acme_api/spikes/" in out


def test_adr_template_uses_placeholder_date_not_fixed_day() -> None:
    text = ADR_TEMPLATE.read_text(encoding="utf-8")
    assert "YYYY-MM-DD" in text
    assert "2026-03-27" not in text


def test_adrs_readme_covers_when_not_to_use() -> None:
    text = ADRS_README.read_text(encoding="utf-8")
    assert "Quando não usar" in text
    assert "spike" in text.lower()
