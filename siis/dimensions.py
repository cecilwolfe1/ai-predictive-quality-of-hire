"""
The ten SIIS dimensions.

Eight are scoreable from transcript and/or scorecard text. Two require
external metadata:
  - evaluation_independence needs ATS scorecard submission timestamps
    vs. panel debrief time.
  - competency_coverage needs the interview guide (which competencies
    were assigned to this interview slot).

The LLM scores the eight text-scoreable dimensions. The other two are
passed in as metadata and joined with the LLM output downstream.

Framework attribution: Williams (2026), "You're Measuring the Wrong Person."
Research basis: Sackett, Zhang, Berry & Lievens (2022).
"""

from dataclasses import dataclass
from typing import Literal

DataSource = Literal["transcript", "scorecard", "transcript+scorecard", "ats_metadata", "interview_guide"]


@dataclass(frozen=True)
class Dimension:
    key: str
    name: str
    criterion: str
    pass_example: str
    fail_example: str
    data_source: DataSource
    llm_scoreable: bool


DIMENSIONS: list[Dimension] = [
    Dimension(
        key="standardized_questions",
        name="Standardized questions",
        criterion=(
            "The interviewer used a predefined set of core questions aligned to "
            "the assigned competencies, rather than an ad-hoc conversation. Small "
            "variations in phrasing are fine; the substance of the questions must "
            "be consistent with a defined question bank for the role."
        ),
        pass_example=(
            "'Opened with the standard behavioral question on handling ambiguity "
            "from the staff-level bank, then moved to the cross-functional "
            "influence question.' — Evidence of a defined question set."
        ),
        fail_example=(
            "'We had a great conversation about her background and what she's "
            "looking for next.' — No evidence of a predefined question set; "
            "describes an unstructured conversation."
        ),
        data_source="transcript",
        llm_scoreable=True,
    ),
    Dimension(
        key="behavioral_evidence",
        name="Behavioral evidence",
        criterion=(
            "Feedback is grounded in specific past actions the candidate described "
            "— what they actually did, in what situation, with what outcome. "
            "Impressions, intuitions, and adjectives about the candidate's "
            "personality do not count as behavioral evidence."
        ),
        pass_example=(
            "'Candidate described leading a migration from monolith to "
            "microservices, walked through specific tradeoffs on data "
            "consistency, and named the rollout sequencing they chose.' — "
            "Concrete past actions."
        ),
        fail_example=(
            "'Seemed really sharp and had great energy. I think he'd thrive "
            "on our team.' — Impression-based, no specific past actions."
        ),
        data_source="transcript+scorecard",
        llm_scoreable=True,
    ),
    Dimension(
        key="job_relevance",
        name="Job relevance",
        criterion=(
            "Comments and ratings are tied to defined role competencies, not "
            "culture fit, rapport, personality reads, or general impressions. "
            "Reasoning should reference the competency being assessed."
        ),
        pass_example=(
            "'Strong on system design competency — walked through consistency "
            "tradeoffs in the payments example.' — Tied to a defined competency."
        ),
        fail_example=(
            "'Great culture fit, we really clicked.' — Rapport-based, not tied "
            "to a role competency."
        ),
        data_source="transcript+scorecard",
        llm_scoreable=True,
    ),
    Dimension(
        key="rating_to_evidence_alignment",
        name="Rating-to-evidence alignment",
        criterion=(
            "The numeric or categorical rating given is supported by the written "
            "justification. A high rating with thin or contradictory evidence "
            "fails; so does a low rating with evidence that actually reads "
            "positively."
        ),
        pass_example=(
            "'Rated 4/4 on influence — provided two concrete examples of "
            "resolving cross-team disagreements with specific outcomes.' — "
            "Rating matches evidence."
        ),
        fail_example=(
            "'Rated 4/4. She was pleasant and engaged.' — Top rating unsupported "
            "by evidence."
        ),
        data_source="scorecard",
        llm_scoreable=True,
    ),
    Dimension(
        key="bias_signal_avoidance",
        name="Bias signal avoidance",
        criterion=(
            "No comparative language ('reminds me of X'), personality adjectives "
            "used as qualifications ('confident,' 'polished,' 'energetic'), "
            "rapport-based cues ('we clicked,' 'got along'), or references to "
            "irrelevant personal traits. These are classic vectors for "
            "similarity bias and should be absent."
        ),
        pass_example=(
            "'Demonstrated the probing-under-pressure competency by naming "
            "specific facilitation choices during the post-incident review.' — "
            "No personality or rapport language."
        ),
        fail_example=(
            "'She was confident and had good energy — reminded me of Sarah "
            "when she joined.' — Personality adjectives plus comparative "
            "language."
        ),
        data_source="transcript+scorecard",
        llm_scoreable=True,
    ),
    Dimension(
        key="scoring_discipline",
        name="Scoring discipline",
        criterion=(
            "The interviewer applied a structured rubric rather than a single "
            "holistic recommendation. Each assigned competency receives its own "
            "rating. A lone 'recommend hire / no hire' verdict without per-"
            "competency scoring fails this dimension."
        ),
        pass_example=(
            "'Influence: 4/4 (exceeds). Ambiguity: 3/4 (meets). Technical "
            "depth: 3/4 (meets).' — Per-competency rubric applied."
        ),
        fail_example=(
            "'Overall: strong hire.' — Single holistic verdict, no rubric."
        ),
        data_source="scorecard",
        llm_scoreable=True,
    ),
    Dimension(
        key="follow_up_probe_quality",
        name="Follow-up probe quality",
        criterion=(
            "When an answer was vague, surface-level, or skipped specifics, the "
            "interviewer probed to surface the underlying behavior. Look for "
            "follow-ups that push for what the candidate actually did, not "
            "hypothetical or general opinions."
        ),
        pass_example=(
            "'When candidate said \"we decided to prioritize,\" interviewer "
            "asked who specifically made the call and what data it was based "
            "on.' — Probes to extract specific behavior."
        ),
        fail_example=(
            "'Candidate gave general answers about leadership philosophy; "
            "interviewer moved to the next question without probing.' — "
            "No probing on vague answers."
        ),
        data_source="transcript",
        llm_scoreable=True,
    ),
    Dimension(
        key="question_form_integrity",
        name="Question form integrity",
        criterion=(
            "Questions are not leading ('you probably handled that by X, right?') "
            "and not hypothetical ('what would you do if...'). Leading questions "
            "telegraph the desired answer; hypotheticals elicit reasoning but "
            "not evidence of past behavior, which is what structured behavioral "
            "interviews are designed to capture."
        ),
        pass_example=(
            "'Tell me about a time you had to make a decision with incomplete "
            "information — walk me through what you did.' — Past-tense "
            "behavioral, not leading."
        ),
        fail_example=(
            "'What would you do if your manager disagreed with your approach?' — "
            "Hypothetical, not behavioral."
        ),
        data_source="transcript",
        llm_scoreable=True,
    ),
    Dimension(
        key="competency_coverage",
        name="Competency coverage",
        criterion=(
            "Every competency assigned to this interview slot was actually "
            "assessed. Requires the interview guide as a reference to score; "
            "the LLM does not score this dimension from text alone."
        ),
        pass_example="",
        fail_example="",
        data_source="interview_guide",
        llm_scoreable=False,
    ),
    Dimension(
        key="evaluation_independence",
        name="Evaluation independence",
        criterion=(
            "The scorecard was submitted before the panel debrief or before "
            "the interviewer saw other interviewers' feedback. Scored from ATS "
            "timestamp data, not from the transcript or scorecard text."
        ),
        pass_example="",
        fail_example="",
        data_source="ats_metadata",
        llm_scoreable=False,
    ),
]

LLM_SCOREABLE = [d for d in DIMENSIONS if d.llm_scoreable]
METADATA_SCOREABLE = [d for d in DIMENSIONS if not d.llm_scoreable]
