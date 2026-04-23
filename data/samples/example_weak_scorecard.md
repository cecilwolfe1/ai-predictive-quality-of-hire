# Sample: weak adherence scorecard

A run of the SIIS scoring prompt against a low-adherence scorecard.
Scored 0/8 — low tier. This is what an unstructured "vibes hire"
recommendation looks like when graded against the framework.

## Input

**Role:** Senior Product Manager
**Competencies assigned to this interview:** product sense, execution, cross-functional influence

**Scorecard under review:**

> Had a great chat with this candidate! Super friendly, easy to talk to,
> clearly motivated. We discussed her background for a bit and then
> talked about what she's looking for in her next role. She said all
> the right things about teamwork and growth, and I could tell she
> really gets it. She reminded me a lot of James when he joined — same
> kind of energy.
>
> I asked her what she'd do if she had to launch a product in a month
> with half the resources, and she gave a really thoughtful answer
> about prioritization. Smart.
>
> I think she'd be a strong culture add and fit well with the team
> vibe.
>
> Recommend hire.

## Scored output

**Result: 0 / 8 dimensions passed — tier: low**

### 1. Standardized questions — FAIL

- **Observation:** The scorecard describes the session as a "great chat," mentions discussing "her background for a bit" and "what she's looking for in her next role," and references only one specific question, framed as "I asked her what she'd do if..." There is no reference to a question bank, a predefined set, or parity with other candidates.
- **Reasoning:** Language like "had a great chat" and "discussed her background for a bit" signals an ad-hoc conversation rather than a structured protocol. The single cited question is introduced as something the interviewer thought of, not drawn from a defined set.
- **Rationale:** No evidence of a predefined question set — the scorecard reads as a free-form conversation with one improvised question.

### 2. Behavioral evidence — FAIL

- **Observation:** Descriptions include "super friendly, easy to talk to, clearly motivated," "said all the right things about teamwork and growth," and "a really thoughtful answer about prioritization." No specific past action, project, decision, or outcome from the candidate's history is described.
- **Reasoning:** Every substantive claim is either a personality impression or a vague characterization of an answer. "Thoughtful answer about prioritization" names the topic but not what she said, did, or decided in any real situation.
- **Rationale:** No concrete past actions are cited — only impressions and a one-line abstraction of an answer to a hypothetical.

### 3. Job relevance — FAIL

- **Observation:** Assigned competencies are product sense, execution, and cross-functional influence. The written comments instead emphasize "culture add," "team vibe," "friendly," "motivated," and "teamwork and growth." Prioritization is mentioned once but not tied explicitly to any of the three competencies.
- **Reasoning:** None of the three assigned competencies are named or structured against in the write-up. The evaluative language centers on fit and demeanor rather than role-defined capability.
- **Rationale:** Commentary is anchored in culture and rapport rather than the three competencies this interview was scoped to assess.

### 4. Rating-to-evidence alignment — FAIL

- **Observation:** There are no per-competency ratings — no numbers, no categorical scales, no rubric levels. The only verdict is "Recommend hire." The supporting evidence is impressionistic ("Smart," "strong culture add," "really gets it").
- **Reasoning:** Alignment requires both a rating and an evidentiary justification. Here the rating structure is absent, and what justification exists is not tied to observable behavior, so there is nothing for the rating to align against in a structured sense.
- **Rationale:** No per-competency ratings exist, and the holistic "recommend hire" rests on vibe-level evidence rather than justified scoring.

### 5. Bias signal avoidance — FAIL

- **Observation:** The scorecard contains "reminded me a lot of James when he joined — same kind of energy" (comparative + energy cue), "super friendly, easy to talk to" (rapport/personality), "strong culture add and fit well with the team vibe" (culture/personality), and "said all the right things" (rapport-based affirmation).
- **Reasoning:** Multiple recognized bias signals are present: comparison to a prior hire, personality adjectives substituting for qualifications, and rapport-based cues. Each on its own would be disqualifying; stacked, they define the evaluation.
- **Rationale:** Explicit comparison to a prior employee plus personality and rapport cues form the backbone of the assessment.

### 6. Scoring discipline — FAIL

- **Observation:** No competency is rated individually. The scorecard ends with a single line, "Recommend hire," with no breakdown across product sense, execution, or cross-functional influence.
- **Reasoning:** Scoring discipline requires a rubric applied per competency. A single holistic recommendation — with no per-competency judgment — is the textbook failure mode.
- **Rationale:** The assessment collapses three assigned competencies into one holistic hire recommendation with no rubric applied.

### 7. Follow-up probe quality — FAIL

- **Observation:** The candidate is described as having given "a really thoughtful answer about prioritization," and as having "said all the right things about teamwork and growth." No follow-up questions, clarifying probes, or requests for specifics are documented.
- **Reasoning:** Both descriptions flag generic or abstract answers that a disciplined interviewer would probe into (what was prioritized, on what basis, who was involved). The write-up instead accepts them at face value.
- **Rationale:** Vague answers are recorded as positives without any evidence of probing for specifics.

### 8. Question form integrity — FAIL

- **Observation:** The only question cited is "what she'd do if she had to launch a product in a month with half the resources."
- **Reasoning:** This is a hypothetical framed in the conditional ("what she'd do if"), not a past-tense behavioral prompt ("tell me about a time you..."). Hypotheticals invite idealized answers rather than evidence of actual behavior.
- **Rationale:** The one documented question is hypothetical rather than a past-tense behavioral prompt.

## Notes on this run

**Stacked bias signals.** The scorer identified four distinct bias signal
types in one scorecard: comparative language (the James reference),
personality adjectives substituting for qualifications, culture/fit
cues, and rapport-based affirmation. Its rationale notes that "stacked,
they define the evaluation" — that operationalized reasoning is the
kind of feedback that makes SIIS useful as a coaching tool. An
interviewer reading this knows exactly what to change.

**Hypothetical vs. behavioral framing.** The scorer correctly distinguished
the conditional "what she'd do if…" from a past-tense behavioral probe
("tell me about a time you…"). The distinction matters because
hypotheticals elicit reasoning, not evidence — exactly what the
question_form_integrity dimension is designed to catch.
