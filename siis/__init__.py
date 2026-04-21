"""SIIS: Structured Interview Integrity Score."""

from .dimensions import DIMENSIONS, LLM_SCOREABLE, METADATA_SCOREABLE, Dimension
from .schemas import DimensionVerdict, ScoringResult, Tier, Verdict
from .scoring import MODEL, SYSTEM_PROMPT, score_interview, score_interview_dry_run

__all__ = [
    "DIMENSIONS",
    "LLM_SCOREABLE",
    "METADATA_SCOREABLE",
    "Dimension",
    "DimensionVerdict",
    "ScoringResult",
    "Tier",
    "Verdict",
    "MODEL",
    "SYSTEM_PROMPT",
    "score_interview",
    "score_interview_dry_run",
]
