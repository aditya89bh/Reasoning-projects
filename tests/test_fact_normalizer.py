"""Tests for shared fact normalization.

Run from the repository root with:
    python -m pytest tests
"""

from shared.fact_normalizer import FactNormalizer


def test_fact_normalizer_maps_symbolic_predicates_to_facts():
    predicates = [
        "object(cup_glass)",
        "type(cup_glass, cup)",
        "material(cup_glass, glass)",
        "fragile(cup_glass, true)",
        "shape(cup_glass, cylinder)",
    ]

    facts = FactNormalizer().normalize_predicates(predicates)

    assert facts == [
        "material_glass",
        "object_cup",
        "object_detected",
        "object_fragile",
        "shape_cylinder",
    ]


def test_fact_normalizer_adds_extra_facts():
    predicates = ["material(cup_glass, glass)"]

    facts = FactNormalizer().normalize_predicates(
        predicates,
        extra_facts=["grip_force_high"],
    )

    assert facts == ["grip_force_high", "material_glass"]


def test_fact_normalizer_supports_custom_mapping():
    normalizer = FactNormalizer()
    normalizer.add_mapping("color(block_red, red)", "color_red")

    facts = normalizer.normalize_predicates(["color(block_red, red)"])

    assert facts == ["color_red"]
