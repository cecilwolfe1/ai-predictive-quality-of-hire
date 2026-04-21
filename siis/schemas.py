"""
Pydantic schemas for SIIS scoring output.

The LLM returns a DimensionVerdict per scoreable dimension. The ScoringResult
wraps all eight LLM verdicts plus the two metadata-scored dimensions, plus
an overall integer score (dimensions passed, out of 10) and an adherence
tier (low / medium / high).

The observation → reasoning → verdict structure is enforced by pydantic.
This matches the forced chain-of-thought from the article: the model must
record what it saw, reason about it, and then commit to a verdict — in
that order. Putting verdict last in the schema matters because the model
generates fields in order, which means the verdict is conditioned on the
observation and reasoning rather than the other way around.
"""

from typing import Literal
from pydantic import BaseModel, Field


Verdict = Literal["pass", "fail"]
Tier = Literal["low", "medium", "high"]


class DimensionVerdict(BaseModel):
    """One dimension's scored output."""

    dimension_key: str = Field(
        description="The snake_case key of the dimension being scored."
    )
    observation: str = Field(
        description=(
            "What the text actually shows — specific phrases, absences, "
            "or patterns observed. Quote or paraphrase directly from the "
            "transcript or scorecard. Do not reason or conclude here."
        )
    )
    reasoning: str = Field(
        description=(
            "How the observation maps to the criterion for this dimension. "
            "This is where the model thinks. Do not state the verdict here."
        )
    )
    verdict: Verdict = Field(
        description="Pass or fail, based on the observation and reasoning above."
    )
    rationale: str = Field(
        description=(
            "A one-sentence coaching rationale the interviewer could read. "
            "Must name the specific evidence (or specific absence of evidence) "
            "that drove the verdict. Do not restate the criterion abstractly."
        )
    )


class ScoringResult(BaseModel):
    """Full SIIS result for one interview."""

    interview_id: str
    interviewer_id: str
    llm_verdicts: list[DimensionVerdict]
    competency_coverage: Verdict | None = Field(
        default=None,
        description="Passed in from interview guide metadata, not scored by LLM.",
    )
    evaluation_independence: Verdict | None = Field(
        default=None,
        description="Passed in from ATS timestamp data, not scored by LLM.",
    )

    @property
    def dimensions_passed(self) -> int:
        passed = sum(1 for v in self.llm_verdicts if v.verdict == "pass")
        if self.competency_coverage == "pass":
            passed += 1
        if self.evaluation_independence == "pass":
            passed += 1
        return passed

    @property
    def total_dimensions(self) -> int:
        total = len(self.llm_verdicts)
        if self.competency_coverage is not None:
            total += 1
        if self.evaluation_independence is not None:
            total += 1
        return total

    @property
    def tier(self) -> Tier:
        """Tiering from the article: 0-4 low, 5-7 medium, 8-10 high."""
        n = self.dimensions_passed
        if n <= 4:
            return "low"
        if n <= 7:
            return "medium"
        return "high"
