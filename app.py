"""
app.py
------
Main entry point for the Resume Revamp System.
Run with: streamlit run app.py

Ties together the extractor, revamper, scorer, and exporter modules
into a clean, beginner-friendly Streamlit interface.
"""

import streamlit as st

from extractor import extract_text_from_pdf
from revamper import revamp_resume
from scorer import keyword_match_score
from exporter import save_as_pdf


# ─── Page Configuration ───────────────────────────────────────────────────────

st.set_page_config(
    page_title="ResumeForge",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ─── Custom Styling ───────────────────────────────────────────────────────────

st.markdown("""
<style>
    /* Import a clean, professional font */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* Page background */
    .stApp {
        background-color: #f4f6fb;
    }

    /* Hero banner */
    .hero {
        background: linear-gradient(135deg, #1e50a0 0%, #162d6b 100%);
        color: white;
        padding: 2.5rem 2rem 2rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .hero h1 {
        font-size: 2.4rem;
        font-weight: 700;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.5px;
    }
    .hero p {
        font-size: 1.05rem;
        opacity: 0.85;
        margin: 0;
    }

    /* Section cards */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem 1.8rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        margin-bottom: 1.2rem;
    }

    /* Score badge */
    .score-badge {
        display: inline-block;
        font-size: 2.2rem;
        font-weight: 700;
        color: #1e50a0;
        border: 3px solid #1e50a0;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        line-height: 74px;
        text-align: center;
        margin: 0.5rem auto;
    }

    /* Keyword chips */
    .chip-green {
        display: inline-block;
        background: #e6f4ea;
        color: #1a7f37;
        border-radius: 20px;
        padding: 3px 12px;
        margin: 3px;
        font-size: 0.82rem;
        font-weight: 500;
    }
    .chip-red {
        display: inline-block;
        background: #fce8e8;
        color: #c0392b;
        border-radius: 20px;
        padding: 3px 12px;
        margin: 3px;
        font-size: 0.82rem;
        font-weight: 500;
    }

    /* Step labels */
    .step-label {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #1e50a0;
        margin-bottom: 0.3rem;
    }

    /* Revamp button */
    div.stButton > button {
        background: linear-gradient(135deg, #1e50a0, #162d6b);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.65rem 2.5rem;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        transition: opacity 0.2s;
    }
    div.stButton > button:hover {
        opacity: 0.88;
    }

    /* Download button */
    div.stDownloadButton > button {
        background: #e6f4ea;
        color: #1a7f37;
        border: 2px solid #1a7f37;
        border-radius: 10px;
        font-weight: 600;
        width: 100%;
        transition: background 0.2s;
    }
    div.stDownloadButton > button:hover {
        background: #d0ecda;
    }
</style>
""", unsafe_allow_html=True)


# ─── Hero Banner ──────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <h1>📄 ResumeForge</h1>
    <p>Upload your resume, paste a job description, and get an AI-powered rewrite in seconds.</p>
</div>
""", unsafe_allow_html=True)


# ─── Input Section ────────────────────────────────────────────────────────────

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="step-label">Step 1 — Upload Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        label="Upload your current resume as a PDF",
        type=["pdf"],
        help="Text-based PDFs work best. Scanned image PDFs are not supported."
    )
    if uploaded_file:
        st.success(f"✅ Uploaded: **{uploaded_file.name}**")

with col2:
    st.markdown('<div class="step-label">Step 2 — Paste Job Description</div>', unsafe_allow_html=True)
    job_description = st.text_area(
        label="Paste the full job description here",
        height=220,
        placeholder="e.g. We are looking for a Python Developer with experience in FastAPI, PostgreSQL, and cloud deployments..."
    )


# ─── Action Button ────────────────────────────────────────────────────────────

st.markdown("<br>", unsafe_allow_html=True)
run_col, _ = st.columns([1, 2])
with run_col:
    revamp_clicked = st.button("🚀 Revamp My Resume")


# ─── Processing & Output ──────────────────────────────────────────────────────

if revamp_clicked:

    # --- Validation ---
    if not uploaded_file:
        st.error("⚠️ Please upload a PDF resume before continuing.")
        st.stop()
    if not job_description.strip():
        st.error("⚠️ Please paste a job description before continuing.")
        st.stop()

    # --- Extract resume text ---
    with st.spinner("Reading your resume..."):
        try:
            resume_text = extract_text_from_pdf(uploaded_file)
        except ValueError as e:
            st.error(f"❌ Could not read the PDF: {e}")
            st.stop()

    # --- Keyword Match Score (optional expansion) ---
    st.markdown("---")
    st.subheader("📊 Keyword Match Score")
    st.caption("How well your *current* resume matches the job description, before the revamp.")

    score_data = keyword_match_score(resume_text, job_description)
    score = score_data["score"]

    score_col, detail_col = st.columns([1, 3], gap="large")

    with score_col:
        # Colour the score based on range
        if score >= 60:
            colour = "#1a7f37"
        elif score >= 35:
            colour = "#b45309"
        else:
            colour = "#c0392b"

        st.markdown(f"""
        <div style="text-align:center; padding: 1rem 0;">
            <div style="font-size:3rem; font-weight:700; color:{colour};">{score}%</div>
            <div style="font-size:0.9rem; color:#666; margin-top:4px;">Match Rate</div>
            <div style="font-size:0.8rem; color:#999;">{len(score_data['matched'])} / {score_data['total']} keywords</div>
        </div>
        """, unsafe_allow_html=True)

    with detail_col:
        if score_data["matched"]:
            st.markdown("**✅ Matched Keywords**")
            chips = " ".join(
                f'<span class="chip-green">{w}</span>'
                for w in score_data["matched"][:20]
            )
            st.markdown(chips, unsafe_allow_html=True)

        if score_data["missing"]:
            st.markdown("**❌ Missing Keywords** *(consider adding these to your resume)*")
            chips = " ".join(
                f'<span class="chip-red">{w}</span>'
                for w in score_data["missing"][:20]
            )
            st.markdown(chips, unsafe_allow_html=True)

    # --- AI Revamp ---
    st.markdown("---")
    st.subheader("✨ AI-Revamped Resume")

    with st.spinner("Gemini is rewriting your resume... this may take a moment."):
        try:
            revamped_text = revamp_resume(resume_text, job_description)
        except (ValueError, RuntimeError) as e:
            st.error(f"❌ Revamp failed: {e}")
            st.stop()

    st.success("✅ Revamp complete!")

    # Before / After comparison
    before_col, after_col = st.columns(2, gap="large")

    with before_col:
        st.markdown("**📋 Original Resume**")
        st.text_area(
            label="original",
            value=resume_text,
            height=450,
            label_visibility="collapsed"
        )

    with after_col:
        st.markdown("**🎯 Revamped Resume**")
        st.text_area(
            label="revamped",
            value=revamped_text,
            height=450,
            label_visibility="collapsed"
        )

    # --- PDF Export (optional expansion) ---
    st.markdown("---")
    st.subheader("💾 Export")
    st.caption("Download your revamped resume as a formatted PDF.")

    try:
        pdf_bytes = save_as_pdf(revamped_text)
        st.download_button(
            label="⬇️ Download Revamped Resume as PDF",
            data=pdf_bytes,
            file_name="revamped_resume.pdf",
            mime="application/pdf",
        )
    except Exception as e:
        st.warning(f"PDF export unavailable: {e}")


# ─── Footer ───────────────────────────────────────────────────────────────────

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; color:#aaa; font-size:0.82rem;'>"
    "ResumeForge · Built with Streamlit & Gemini API · Python Advanced Class Project"
    "</div>",
    unsafe_allow_html=True
)
