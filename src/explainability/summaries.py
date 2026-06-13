"""Plain-language explainability summaries for ClariPulse™."""
from __future__ import annotations


def clinical_explanation() -> str:
    """Return a reusable clinician-friendly explanation example."""
    return (
        "The elevated risk is primarily driven by age, abnormal vital signs, elevated lactate, "
        "renal dysfunction markers, and recent ICU exposure. Clinical review is recommended."
    )


def executive_explanation() -> str:
    """Return a reusable executive-friendly explanation example."""
    return (
        "High-risk patient volume is concentrated among encounters with physiological instability, "
        "complex comorbidity burden, and critical-care exposure. Targeted intervention workflows may reduce downstream risk."
    )
