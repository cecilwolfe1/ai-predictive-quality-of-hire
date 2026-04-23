# Sample: mixed adherence scorecard

This is a real run of the SIIS scoring prompt against a deliberately
mixed-adherence scorecard. The prompt was run in Claude.ai (same model
family as the production scoring module would use) to validate that
the scoring logic produces coaching-grade output without needing to
burn API credits during development.

## Input

**Role:** Senior Software Engineer
**Competencies assigned to this interview:** system design, coding, cross-functional influence

**Scorecard under review:**

> Interviewed Priya today. We had a really good conversation — she walked
> me through a migration project she led at her last company where they
> moved from a monolithic Rails app to microservices. She explained how
> she decided to start with the read-heavy services first and talked
> through the data consistency tradeoffs they evaluated. I asked her what
> led to that specific sequencing and she gave me a concrete answer about
> traffic patterns and blast radius.
>
> On the system design piece, I was less impressed. She's clearly smart
> and has great energy, and I can tell she'd get along well with the team
> — she reminded me a bit of Kavya when she first joined. But I didn't
> get to ask about distributed systems depth the way I wanted.
>
> Rating: 4/4. Strong hire, would love to have her on the team.

## Scored output

**Result: 2 / 8 dimensions passed — tier: low**

### 1. Standardized questions — FAIL

- **Observation:** No reference to a question bank, predefined list, or standard prompts. Opening framing is "We had a really good conversation," and the only question explicitly described is a reactive follow-up ("I asked her what led to that specific sequencing").
- **Reasoning:** The criterion requires evidence the interviewer drew from a predefined question set. Conversational framing plus zero references to standard prompts indicates an ad-hoc interview.
- **Rationale:** Scorecard reads as a free-form conversation with no indication that competencies were probed through a predetermined question set.

### 2. Behavioral evidence — FAIL

- **Observation:** The migration discussion contains genuine behavioral specifics — Rails monolith to microservices, sequencing read-heavy services first, tradeoffs on data consistency, reasoning about traffic patterns and blast radius. However, the system design assessment is impressionistic ("clearly smart and has great energy"), and the final 4/4 rating is not tied to any described past action.
- **Reasoning:** The criterion asks whether feedback is grounded in specific past actions. Partial behavioral grounding exists for the migration story, but the decisive rating-driving content is impressions and rapport rather than behavior.
- **Rationale:** One competency area is behaviorally grounded, but the overall recommendation leans on "clearly smart" and "great energy" rather than described actions.

### 3. Job relevance — FAIL

- **Observation:** Assigned competencies are system design, coding, and cross-functional influence. Coding is never mentioned. Cross-functional influence is not explicitly assessed. System design is partially touched via the migration example, but the interviewer openly concedes "I didn't get to ask about distributed systems depth." Meanwhile, comments about "great energy," "get along well with the team," and the Kavya comparison are culture/fit signals.
- **Reasoning:** A job-relevant scorecard would route observations into the defined competencies. Two of three competencies are unaddressed, and a material portion of the narrative is about fit and personality rather than role requirements.
- **Rationale:** Coding and influence are never evaluated, and the strongest qualitative language is about fit rather than the three assigned competencies.

### 4. Rating-to-evidence alignment — FAIL

- **Observation:** Final rating is "4/4. Strong hire." The interviewer explicitly states they were "less impressed" on system design, "didn't get to ask about distributed systems depth," and provides no coding or influence evidence at all.
- **Reasoning:** A 4/4 top rating requires evidence across the assessed competencies. The written justification documents gaps and admitted unasked questions, which directly contradicts a maximum score.
- **Rationale:** Rating of 4/4 is incompatible with the interviewer's own admissions of unassessed competencies and an unimpressive system design segment.

### 5. Bias signal avoidance — FAIL

- **Observation:** "she reminded me a bit of Kavya when she first joined" (comparison to another employee), "great energy" (personality adjective used as qualification), "clearly smart" (trait attribution without behavioral anchor), "get along well with the team" (rapport/fit cue).
- **Reasoning:** The criterion is violated when comparative, personality, or rapport-based language appears as justification. Multiple such phrases appear, and one drives directly toward the hiring recommendation.
- **Rationale:** Comparison to "Kavya," "great energy," and "get along well with the team" are textbook bias signals appearing as reasons to hire.

### 6. Scoring discipline — FAIL

- **Observation:** Three competencies were assigned (system design, coding, cross-functional influence). The scorecard produces a single holistic rating: "4/4. Strong hire." No per-competency scores.
- **Reasoning:** The criterion requires a rubric applied per competency. One collapsed rating across all dimensions is the opposite pattern.
- **Rationale:** One holistic "4/4" replaces what should have been three independent competency ratings.

### 7. Follow-up probe quality — PASS

- **Observation:** When the candidate described the migration sequencing, the interviewer probed: "I asked her what led to that specific sequencing and she gave me a concrete answer about traffic patterns and blast radius."
- **Reasoning:** The criterion requires probing to surface specific behavior when an answer risks being vague. The documented probe does exactly this and yields concrete detail about the candidate's actual reasoning.
- **Rationale:** Interviewer documented a targeted follow-up that pushed the sequencing discussion from general to specific.

### 8. Question form integrity — PASS

- **Observation:** The one documented question — "what led to that specific sequencing" — is a past-tense behavioral probe about a decision the candidate actually made. No hypothetical or leading phrasing appears anywhere in the scorecard.
- **Reasoning:** The criterion is about the form of questions used. The only visible question meets the behavioral standard; nothing in the text suggests hypothetical or leading questions were asked.
- **Rationale:** The single documented question is past-tense behavioral form; no leading or hypothetical phrasing is visible.

## Notes on this run

Two observations worth preserving for future prompt iteration:

**Strictness calibration.** This scorecard scored 2/8 (low tier). A reasonable argument could be made for 3/8 depending on how the behavioral_evidence criterion is interpreted — the migration story contains genuine behavioral specifics, even though the rating isn't driven by that evidence. This is a real prompt-engineering finding: the criterion says "Feedback is grounded in specific past actions," which is ambiguous between "feedback contains grounded evidence" and "the recommendation is grounded in evidence." An I/O psychologist labeling this dataset could go either way. Resolving this ambiguity in the criterion wording would be the right next step.

**Strength of bias detection.** The scorer caught four distinct bias signals — comparative ("Kavya"), personality-as-qualification ("great energy"), trait attribution without anchor ("clearly smart"), and rapport/fit cue ("get along well with the team") — and correctly noted that these appear "as reasons to hire." This is the kind of operationalized reasoning that makes SIIS useful as a coaching tool rather than a blunt flag.

**Coaching rationales.** Every rationale names specific evidence rather than restating the criterion. This is the single most important property for the scorer to have — an interviewer reading their feedback should know exactly what phrase to change next time. Goal achieved on this run.
