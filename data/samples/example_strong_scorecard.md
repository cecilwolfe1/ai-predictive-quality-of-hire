# Sample: strong adherence scorecard

A run of the SIIS scoring prompt against a high-adherence scorecard.
Scored 8/8 — high tier. This is what structured interviewing looks
like when it's being done properly.

## Input

**Role:** Staff Software Engineer
**Competencies assigned to this interview:** technical leadership, ambiguity, cross-functional influence

**Scorecard under review:**

> Used the standard behavioral question bank for staff-level ambiguity
> and cross-functional influence. Candidate described a specific incident
> running a post-incident review across three teams — named the
> stakeholders (infra lead, two product managers, SRE on-call), described
> the facilitation choices, walked through the decision to split
> remediation into two workstreams based on risk profile. Probed twice
> on how they handled the disagreement with the infra lead about the
> rollback threshold; answer was concrete — brought in error-rate metrics
> from the last three incidents and escalated the framing, not the
> decision itself.
>
> Technical leadership: 4/4 (exceeds). Demonstrated through the
> remediation split decision, specific use of data to escalate framing
> rather than authority.
>
> Ambiguity: 3/4 (meets). Clear decision-making under incomplete
> information during the incident; defaulted to safer rollback when
> data was thin.
>
> Cross-functional influence: 4/4 (exceeds). Multi-team incident
> resolution with named stakeholders and measurable outcome (MTTR
> reduced on follow-up incident).
>
> Scorecard submitted before panel debrief per ATS.

## Scored output

**Result: 8 / 8 dimensions passed — tier: high**

### 1. Standardized questions — PASS

- **Observation:** The scorecard opens with "Used the standard behavioral question bank for staff-level ambiguity and cross-functional influence."
- **Reasoning:** This explicitly references a predefined question set tied to the competencies assigned, which is the core signal for this dimension.
- **Rationale:** Direct reference to a named question bank scoped to the assigned competencies satisfies the standardization criterion.

### 2. Behavioral evidence — PASS

- **Observation:** The write-up cites a specific past incident — a post-incident review across three teams, named roles (infra lead, two PMs, SRE on-call), the decision to split remediation into two workstreams, and the use of error-rate metrics from the last three incidents to reframe a disagreement.
- **Reasoning:** Every judgment is anchored to concrete actions the candidate described taking, not impressions or adjectives about the person.
- **Rationale:** Feedback is grounded in named stakeholders, specific facilitation choices, and a described decision mechanism rather than personality reads.

### 3. Job relevance — PASS

- **Observation:** Each rated item maps to one of the three assigned competencies (technical leadership, ambiguity, cross-functional influence), and the evidence cited for each is tied to that competency rather than to rapport or culture.
- **Reasoning:** No references to culture fit, likability, or personal chemistry appear; the commentary stays inside the defined role competencies for a staff-level engineer.
- **Rationale:** Commentary is tied directly to the three pre-defined competencies with no drift into culture-fit or rapport territory.

### 4. Rating-to-evidence alignment — PASS

- **Observation:** Technical leadership 4/4 is justified by the remediation-split decision and using data to escalate framing; ambiguity 3/4 is justified by decision-making under incomplete information and defaulting to safer rollback; cross-functional influence 4/4 is justified by multi-team resolution with named stakeholders and a measurable MTTR outcome.
- **Reasoning:** Each rating points to specific behavioral evidence from earlier in the write-up, and the lower rating on ambiguity is consistent with slightly thinner evidence (one decision point vs. multiple).
- **Rationale:** Each numeric rating is paired with concrete, rating-specific evidence rather than generic praise.

### 5. Bias signal avoidance — PASS

- **Observation:** No personality adjectives ("sharp," "confident," "great energy"), no comparisons to other employees, no rapport or chemistry language, and no references to irrelevant personal traits appear anywhere in the text.
- **Reasoning:** The write-up stays on observable behavior and decisions; absence of bias-coded language is itself the observation here, and that absence is what the dimension requires.
- **Rationale:** The scorecard is free of comparative, personality-based, or rapport-driven language throughout.

### 6. Scoring discipline — PASS

- **Observation:** Three separate ratings are recorded — Technical leadership 4/4, Ambiguity 3/4, Cross-functional influence 4/4 — with distinct justifications, and no single holistic "hire/no-hire" verdict is collapsed on top.
- **Reasoning:** A structured rubric is applied per competency rather than a blanket recommendation, which is the definition of scoring discipline.
- **Rationale:** Per-competency ratings with independent justifications satisfy the rubric-discipline criterion.

### 7. Follow-up probe quality — PASS

- **Observation:** "Probed twice on how they handled the disagreement with the infra lead about the rollback threshold; answer was concrete — brought in error-rate metrics from the last three incidents and escalated the framing, not the decision itself."
- **Reasoning:** The interviewer explicitly probed on a specific moment to surface behavioral detail, and documented what the probe produced.
- **Rationale:** Documented double-probe on the infra-lead disagreement shows the interviewer pushed for specific behavior rather than accepting a general answer.

### 8. Question form integrity — PASS

- **Observation:** The scorecard references behavioral questions from a bank and describes the candidate recounting a specific past incident ("described," "named," "walked through"). There are no hypothetical or leading question stems documented.
- **Reasoning:** The evidence is all past-tense recounting, which is consistent with past-tense behavioral question form. The dimension does not require the literal questions to be quoted; the pattern of answers is a reasonable signal of form.
- **Rationale:** All cited responses are past-tense recollections of a specific incident, consistent with behavioral rather than hypothetical question form.

## Notes on this run

**Inferential reasoning on question_form_integrity.** The scorer correctly
infers past-tense behavioral question form from the pattern of the
candidate's answers, even though the literal questions aren't quoted in
the scorecard. This is the kind of inferential move a human I/O
practitioner would make, and it shows the scorer isn't just
pattern-matching on specific phrases.

**Consistency with the mixed scorecard.** This scorecard's migration
story passes behavioral_evidence; the mixed scorecard's migration
story failed behavioral_evidence because the rating was driven by
impressions, not because behavioral evidence was absent. Different
situation, different verdict — the scorer is showing calibration
consistency across cases.
