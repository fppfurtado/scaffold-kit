"""Regression: domain.md template must avoid invalid Copier/Jinja filters and domain-specific examples."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

DOMAIN_TEMPLATE = (
    REPO_ROOT
    / "template"
    / "docs"
    / "{% if include_domain_model %}domain.md.jinja{% endif %}"
)


def test_domain_template_avoids_invalid_now_date_filter() -> None:
    """Copier does not provide `now | date(...)`; literal braces would leak into generated projects."""
    text = DOMAIN_TEMPLATE.read_text(encoding="utf-8")
    assert "now | date" not in text
    assert "{{ now" not in text


def test_domain_template_uses_static_last_updated_placeholder() -> None:
    text = DOMAIN_TEMPLATE.read_text(encoding="utf-8")
    assert "(preencha a data da última atualização)" in text


def test_domain_template_vocabulary_table_is_generic() -> None:
    """Avoid project-specific example terms in the ubiquitous language table."""
    text = DOMAIN_TEMPLATE.read_text(encoding="utf-8")
    assert "Conciliação" not in text
    assert "*(termo do domínio 1)*" in text
    assert "*(termo do domínio 2)*" in text
