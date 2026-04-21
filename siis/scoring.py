"""
SIIS scoring module.

Takes a transcript and/or scorecard string plus interview metadata, returns
a ScoringResult with per-dimension observation, reasoning, verdict, and
rationale.

Design choices worth noting:

  1. Tool use for structured output. We define a single tool
     `submit_siis_scoring` whose input schema is the eight-verdict array.
     The model is forced to call this tool, which gives us schema-validated
     JSON instead of free-form text we have to parse. More reliable than
     JSON-mode prompting, and this pattern is what production systems use.

  2. Forced observe → reason → verdict ordering. The pydantic schema for
     each dimension puts observation first, then reasoning, then verdict.
     Autoregressive models generate fields in order, so verdict is
     conditioned on the preceding work rather than decided first and
     rationalized after.

  3. Calibration examples per dimension. Every dimension ships with a
     pass example and a fail example in the system prompt. Anchors the
     model's threshold and dramatically reduces drift on ambiguous cases.

  4. No hiring-decision context passed to the model. The model does not
     see whether the candidate was hired, rejected, or any candidate
     characteristics. SIIS scores the interviewer, not the interviewee.
     If the model knew the outcome it could be tempted to reason backward
     from "this hire worked out" to "the interview must have been well-run."
"""

from __future__ import annotations

import json
from typing import Optional

from anthropic import Anthropic

from .dimensions import LLM_SCOREABLE, Dimension
from .schemas import DimensionVerdict, ScoringResult, Verdict


MODEL = "claude-opus-4-7"
MAX_TOKENS = 4096


def _dimension_block(d: Dimension) -> str:
    """Render one dimension as a block of the system prompt."""
    return (
        f"Dimension: {d.name}\n"
        f"  Key: {d.key}\n"
        f"  Criterion: {d.criterion}\n"
        f"  Example of a pass: {d.pass_example}\n"
        f"  Example of a fail: {d.fail_example}\n"
    )


SYSTEM_PROMPT = """You are a scoring engine for the Structured Interview Integrity Score (SIIS).

SIIS measures how well an interviewer adhered to structured interviewing best practices. You are scoring the interviewer, not the candidate. Ignore any signal about whether the candidate was strong or weak — that is not what this framework measures.

You will receive a transcript, a written scorecard, or both. Score each of the eight dimensions below independently. For each dimension, you must:

  1. Observe: quote or paraphrase the specific phrases, patterns, or absences in the text that are relevant to this dimension. If the dimension requires evidence that is absent, say so explicitly — absence is itself an observation.

  2. Reason: explain how the observation maps to the criterion. This is where you think through edge cases. Do not state the verdict yet.

  3. Verdict: pass or fail. Binary, no partial credit.

  4. Rationale: one sentence of coaching-grade feedback that names the specific evidence (or absence of evidence) that drove the verdict. An interviewer reading this should know exactly what to do differently next time.

Important scoring guidance:

  - Fail is the default when evidence is absent. A dimension does not pass because nothing disconfirms it; it passes because something confirms it.
  - Do not infer quality from tone or polish. A confidently-written but impression-based scorecard fails behavioral_evidence.
  - A dimension can fail even if most of the interview was fine. One clear bias signal fails bias_signal_avoidance; one leading question fails question_form_integrity.
  - Do not penalize the same evidence twice. If "great culture fit" is the only issue, it fails job_relevance and bias_signal_avoidance — that is two dimensions, scored independently, not double-counting.
  - You are not deciding whether the interviewer is a good or bad interviewer overall. You are scoring this specific interview against the criterion for each dimension.

The eight dimensions you will score:

""" + "\n".join(_dimension_block(d) for d in LLM_SCOREABLE) + """

Return your scoring by calling the submit_siis_scoring tool. You must score all eight dimensions. Do not skip any.
"""


def _build_scoring_tool() -> dict:
    """Build the tool schema that forces structured output."""
    return {
        "name": "submit_siis_scoring",
        "description": (
            "Submit SIIS scoring for all eight LLM-scoreable dimensions. "
            "You must include one verdict per dimension."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "verdicts": {
                    "type": "array",
                    "minItems": len(LLM_SCOREABLE),
                    "maxItems": len(LLM_SCOREABLE),
                    "items": {
                        "type": "object",
                        "properties": {
                            "dimension_key": {
                                "type": "string",
                                "enum": [d.key for d in LLM_SCOREABLE],
                            },
                            "observation": {"type": "string"},
                            "reasoning": {"type": "string"},
                            "verdict": {
                                "type": "string",
                                "enum": ["pass", "fail"],
                            },
                            "rationale": {"type": "string"},
                        },
                        "required": [
                            "dimension_key",
                            "observation",
                            "reasoning",
                            "verdict",
                            "rationale",
                        ],
                    },
                }
            },
            "required": ["verdicts"],
        },
    }


def _build_user_message(transcript: str | None, scorecard: str | None, role: str) -> str:
    if not transcript and not scorecard:
        raise ValueError("Need at least one of transcript or scorecard.")
    parts = [f"Role being interviewed for: {role}", ""]
    if transcript:
        parts.append("=== INTERVIEW TRANSCRIPT ===")
        parts.append(transcript.strip())
        parts.append("")
    if scorecard:
        parts.append("=== INTERVIEWER'S WRITTEN SCORECARD ===")
        parts.append(scorecard.strip())
        parts.append("")
    parts.append("Score all eight dimensions via the submit_siis_scoring tool.")
    return "\n".join(parts)


def score_interview(
    *,
    interview_id: str,
    interviewer_id: str,
    role: str,
    transcript: Optional[str] = None,
    scorecard: Optional[str] = None,
    competency_coverage: Optional[Verdict] = None,
    evaluation_independence: Optional[Verdict] = None,
    client: Optional[Anthropic] = None,
) -> ScoringResult:
    """
    Score a single interview.

    transcript and scorecard are both optional but at least one must be
    provided. competency_coverage and evaluation_independence are passed
    in from metadata (interview guide, ATS timestamps) — they are not
    scored by the LLM.
    """
    if client is None:
        client = Anthropic()

    tool = _build_scoring_tool()
    user_message = _build_user_message(transcript, scorecard, role)

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        tools=[tool],
        tool_choice={"type": "tool", "name": "submit_siis_scoring"},
        messages=[{"role": "user", "content": user_message}],
    )

    tool_use_block = next(
        (block for block in response.content if block.type == "tool_use"),
        None,
    )
    if tool_use_block is None:
        raise RuntimeError(
            f"Model did not call the scoring tool. Response: {response.content}"
        )

    raw_verdicts = tool_use_block.input["verdicts"]
    verdicts = [DimensionVerdict.model_validate(v) for v in raw_verdicts]

    returned_keys = {v.dimension_key for v in verdicts}
    expected_keys = {d.key for d in LLM_SCOREABLE}
    if returned_keys != expected_keys:
        missing = expected_keys - returned_keys
        extra = returned_keys - expected_keys
        raise RuntimeError(
            f"Dimension mismatch. Missing: {missing}. Extra: {extra}."
        )

    return ScoringResult(
        interview_id=interview_id,
        interviewer_id=interviewer_id,
        llm_verdicts=verdicts,
        competency_coverage=competency_coverage,
        evaluation_independence=evaluation_independence,
    )


def score_interview_dry_run(
    *,
    interview_id: str,
    interviewer_id: str,
    role: str,
    transcript: Optional[str] = None,
    scorecard: Optional[str] = None,
) -> dict:
    """
    Return what would be sent to the model without actually calling it.
    Useful for prompt inspection and for running tests offline.
    """
    return {
        "model": MODEL,
        "system_prompt_chars": len(SYSTEM_PROMPT),
        "system_prompt_preview": SYSTEM_PROMPT[:500] + "...",
        "user_message": _build_user_message(transcript, scorecard, role),
        "tool_schema": _build_scoring_tool(),
        "interview_id": interview_id,
        "interviewer_id": interviewer_id,
    }
