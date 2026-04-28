"""
SIIS demo app — interactive portfolio surface for the scoring framework.

Runs in two modes:

  1. No API key (default). Reads the three committed sample scorecards,
     lets the user browse them with full per-dimension reasoning, and
     allows pasting custom scorecards to see what would be sent to the
     model. Zero cost, zero credentials.

  2. With API key. Same as above, but the "Score Your Own" page actually
     calls the SIIS scorer instead of just previewing the prompt. Key is
     read from ANTHROPIC_API_KEY environment variable; never asked for
     in the UI. This is for the developer running locally, not for
     public users of the hosted demo.

Deployable to Streamlit Cloud directly from GitHub. Hosted demo runs in
no-API-key mode by default.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).parent
SAMPLES_DIR = REPO_ROOT / "data" / "samples"

SAMPLE_FILES = {
    "Strong adherence (8/8 — high)": "example_strong_scorecard.md",
    "Mixed adherence (2/8 — low)": "example_mixed_scorecard.md",
    "Weak adherence (0/8 — low)": "example_weak_scorecard.md",
}


# --- helpers --------------------------------------------------------------


def has_api_key() -> bool:
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


def load_sample(filename: str) -> str:
    path = SAMPLES_DIR / filename
    if not path.exists():
        return f"_Sample file not found: {filename}_"
    return path.read_text(encoding="utf-8")


def parse_sample(markdown: str) -> dict:
    """Pull the input scorecard, the result line, and the per-dimension blocks."""
    # Normalize line endings — Windows uses \r\n which breaks naive regex.
    markdown = markdown.replace("\r\n", "\n").replace("\r", "\n")

    out = {"input": "", "result": "", "dimensions": []}

    input_match = re.search(
        r"## Input\s*\n(.*?)(?=\n## Scored output)",
        markdown,
        re.DOTALL,
    )
    if input_match:
        out["input"] = input_match.group(1).strip()

    result_match = re.search(r"\*\*Result:.*?\*\*", markdown)
    if result_match:
        out["result"] = result_match.group(0)

    # Match em-dash (—), en-dash (–), or hyphen (-) between name and verdict.
    dim_pattern = re.compile(
        r"### \d+\.\s+(.+?)\s+[—–-]\s+(PASS|FAIL)\s*\n(.*?)(?=\n### |\n## |\Z)",
        re.DOTALL,
    )
    for match in dim_pattern.finditer(markdown):
        out["dimensions"].append({
            "name": match.group(1).strip(),
            "verdict": match.group(2),
            "body": match.group(3).strip(),
        })
    return out


def render_dimension(dim: dict) -> None:
    color = "#1a7f37" if dim["verdict"] == "PASS" else "#cf222e"
    bg = "#ddf4dd" if dim["verdict"] == "PASS" else "#ffd7d5"
    icon = "✓" if dim["verdict"] == "PASS" else "✗"
    st.markdown(
        f"""
        <div style='background:{bg};border-left:4px solid {color};
                    padding:0.75rem 1rem;border-radius:6px;margin:0.5rem 0;'>
          <div style='font-weight:600;color:{color};margin-bottom:0.25rem;'>
            {icon} &nbsp; {dim['name']} — {dim['verdict']}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(dim["body"])


# --- pages ----------------------------------------------------------------


def page_about() -> None:
    st.title("SIIS — Structured Interview Integrity Score")
    st.markdown("**Quality of hire has always measured the wrong person.**")

    st.markdown("""
Most organizations measure hiring quality by looking at the candidate —
first-year performance, 12-month retention, hiring manager satisfaction.
All lagging. All aimed at the wrong target. The strongest predictor of
whether a hire will succeed isn't a candidate attribute. It's whether
the interviewer actually ran a structured interview or just had a
conversation and called it one.

Meta-analytic research has been clear on this for 30 years. Sackett,
Zhang, Berry & Lievens (2022) rank structured interviews (r = .42) as
the single strongest selection method available — above cognitive
ability tests, work samples, and every other method evaluated. The
barrier was never knowledge. It was that adherence was nearly
impossible to measure at scale.

This demo explores using an LLM to score interviewer adherence to
structured interviewing best practices, across ten dimensions, from
transcripts and scorecards. The framework (SIIS) comes from Zach
Williams's writing; this is my proof-of-concept implementation.
    """)

    st.subheader("The ten dimensions")

    dims = [
        ("Standardized questions", "Did the interviewer use a predefined question set?", "Transcript"),
        ("Behavioral evidence", "Is feedback grounded in specific past actions?", "Transcript + scorecard"),
        ("Job relevance", "Are comments tied to defined competencies?", "Transcript + scorecard"),
        ("Rating-to-evidence alignment", "Does the score match the written justification?", "Scorecard"),
        ("Bias signal avoidance", "No comparative language, personality adjectives, rapport cues?", "Transcript + scorecard"),
        ("Scoring discipline", "Per-competency rubric, not a lone holistic verdict?", "Scorecard"),
        ("Follow-up probe quality", "Did the interviewer probe on vague answers?", "Transcript"),
        ("Question form integrity", "No leading or hypothetical questions?", "Transcript"),
        ("Competency coverage", "Were all assigned competencies assessed?", "Interview guide"),
        ("Evaluation independence", "Scorecard submitted before panel debrief?", "ATS timestamps"),
    ]
    cols = st.columns([2, 4, 2])
    cols[0].markdown("**Dimension**")
    cols[1].markdown("**What it checks**")
    cols[2].markdown("**Scored from**")
    for name, desc, source in dims:
        c = st.columns([2, 4, 2])
        c[0].markdown(name)
        c[1].markdown(desc)
        c[2].markdown(f"_{source}_")

    st.markdown("""
The first eight are scored by the LLM from text. The last two require
external metadata (interview guide, ATS timestamps). The framework
doesn't pretend the model can score what it can't see.
    """)

    st.subheader("What this is — and isn't")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
**This is:**
- A coaching tool for interviewers
- Scoring of the interviewer, not the candidate
- A nightly batch process, run after the hiring decision
- Per-dimension feedback with specific, actionable rationale
        """)
    with col_b:
        st.markdown("""
**This is not:**
- A hiring decision input
- Real-time interviewer surveillance
- A replacement for human calibration
- Trained on real interview data (this POC uses synthetic scorecards)
        """)


def page_examples() -> None:
    st.title("Scored examples")
    st.markdown(
        "Three real runs of the SIIS scoring prompt against scorecards "
        "spanning the adherence spectrum. Click between them to see how "
        "the scorer reasons about strong, mixed, and weak adherence."
    )

    label = st.selectbox(
        "Choose an example to inspect",
        list(SAMPLE_FILES.keys()),
        index=0,
    )
    raw = load_sample(SAMPLE_FILES[label])
    parsed = parse_sample(raw)

    if parsed["result"]:
        st.markdown(f"### {parsed['result']}")

    col_input, col_output = st.columns([1, 1])

    with col_input:
        st.markdown("#### Input scorecard")
        st.markdown(parsed["input"])

    with col_output:
        st.markdown("#### Per-dimension scoring")
        if not parsed["dimensions"]:
            st.warning("No dimensions parsed — sample file format may have changed.")
        else:
            for dim in parsed["dimensions"]:
                render_dimension(dim)


def page_score_your_own() -> None:
    st.title("Score your own scorecard")
    st.markdown(
        "Paste an interviewer's written scorecard below. The eight "
        "LLM-scoreable dimensions will be evaluated and per-dimension "
        "verdicts shown."
    )

    if not has_api_key():
        st.info(
            "**Demo mode** — no `ANTHROPIC_API_KEY` is set, so this page "
            "shows what the scoring prompt would send to Claude rather "
            "than calling the API. To run live scoring, clone the repo, "
            "set your key in `.env`, and run `streamlit run app.py` locally."
        )

    role = st.text_input(
        "Role being interviewed for",
        value="Senior Software Engineer",
    )
    competencies = st.text_input(
        "Competencies assigned to this interview (comma-separated)",
        value="system design, coding, cross-functional influence",
    )
    scorecard_text = st.text_area(
        "Scorecard text",
        height=200,
        value=(
            "Candidate seemed really sharp and had great energy. "
            "Good culture fit and would get along with the team. "
            "Recommend hire."
        ),
    )

    if st.button("Score this scorecard", type="primary"):
        if not scorecard_text.strip():
            st.error("Please paste a scorecard above.")
            return

        if has_api_key():
            with st.spinner("Scoring via Anthropic API..."):
                try:
                    from siis import score_interview
                    result = score_interview(
                        interview_id="demo_001",
                        interviewer_id="demo_user",
                        role=role,
                        scorecard=scorecard_text,
                    )
                    st.success(
                        f"**{result.dimensions_passed}/{result.total_dimensions} "
                        f"dimensions passed — tier: {result.tier}**"
                    )
                    for v in result.llm_verdicts:
                        render_dimension({
                            "name": v.dimension_key.replace("_", " ").title(),
                            "verdict": v.verdict.upper(),
                            "body": (
                                f"**Observation:** {v.observation}\n\n"
                                f"**Reasoning:** {v.reasoning}\n\n"
                                f"**Rationale:** {v.rationale}"
                            ),
                        })
                except Exception as e:
                    st.error(f"API call failed: {e}")
        else:
            try:
                from siis import score_interview_dry_run
                preview = score_interview_dry_run(
                    interview_id="demo_001",
                    interviewer_id="demo_user",
                    role=role,
                    scorecard=scorecard_text,
                )
                st.markdown("#### Prompt preview (no API call made)")
                st.markdown("**Model:** `" + preview["model"] + "`")
                st.markdown("**System prompt size:** " + f"{preview['system_prompt_chars']:,} chars")
                with st.expander("System prompt (first 500 chars)"):
                    st.code(preview["system_prompt_preview"], language="markdown")
                with st.expander("User message"):
                    st.code(preview["user_message"], language="markdown")
                with st.expander("Tool schema (forces structured output)"):
                    st.json(preview["tool_schema"])
            except Exception as e:
                st.error(f"Dry run failed: {e}")


# --- main -----------------------------------------------------------------


def main() -> None:
    st.set_page_config(
        page_title="SIIS — Structured Interview Integrity Score",
        page_icon="📋",
        layout="wide",
    )

    st.sidebar.title("SIIS demo")
    st.sidebar.markdown(
        "_Scoring interviewer adherence to structured interviewing "
        "best practices._"
    )
    page = st.sidebar.radio(
        "Navigate",
        ["About SIIS", "Scored examples", "Score your own"],
        index=0,
    )

    st.sidebar.markdown("---")
    if has_api_key():
        st.sidebar.success("API key detected — live scoring enabled.")
    else:
        st.sidebar.info("No API key — demo mode (preview only).")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "[GitHub repo](https://github.com/cecilwolfe1/ai-predictive-quality-of-hire) · "
        "Built by [@cecilwolfe1](https://github.com/cecilwolfe1)"
    )

    if page == "About SIIS":
        page_about()
    elif page == "Scored examples":
        page_examples()
    else:
        page_score_your_own()


if __name__ == "__main__":
    main()
