"""Smoke tests for the integrated reasoning scaffold.

These tests intentionally avoid deep import execution across project-local `src`
packages. They verify that the integration entrypoint and result artifact exist
and contain the expected architecture markers.

Run from the repository root with:
    python -m pytest tests
"""

from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_integrated_demo_entrypoint_exists():
    path = REPO_ROOT / "integrated_demo" / "run_integrated_demo.py"

    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "Integrated Reasoning Demo" in content
    assert "FactNormalizer" in content
    assert "run_sparse_reasoning" in content
    assert "run_concept_memory" in content
    assert "run_rule_induction" in content


def test_integrated_trace_documents_full_loop():
    path = REPO_ROOT / "integrated_demo" / "results" / "integrated_trace.md"

    assert path.exists()
    content = path.read_text(encoding="utf-8")
    assert "Project 03: Visual-to-Symbolic State" in content
    assert "Shared Fact Normalizer" in content
    assert "Project 02: Memory-Backed Concepts" in content
    assert "Project 01: Sparse Logical Reasoning" in content
    assert "Project 04: Rule Induction" in content
    assert "state → normalized facts → memory → rules → learning → trace" in content
