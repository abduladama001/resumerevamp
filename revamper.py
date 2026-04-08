"""
revamper.py
-----------
Handles all communication with the Gemini API via the google-genai package.
Takes the extracted resume text and a job description, then returns
an AI-rewritten version of the resume tailored to the role.
"""

import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Initialise the Gemini client once at module level
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def revamp_resume(resume_text: str, job_description: str) -> str:
    """
    Send the resume and job description to Gemini and return a rewritten resume.

    Args:
        resume_text:      The plain text extracted from the uploaded PDF resume.
        job_description:  The job description the user is targeting.

    Returns:
        A string containing the AI-rewritten resume.

    Raises:
        RuntimeError: If the API call fails or returns an empty response.
    """
    if not resume_text.strip():
        raise ValueError("Resume text is empty. Please upload a valid resume.")
    if not job_description.strip():
        raise ValueError("Job description is empty. Please paste a job description.")

    prompt = f"""
You are an expert professional resume writer with 10+ years of experience helping
candidates land jobs at top companies.

Your task is to rewrite the candidate's resume so it is strongly tailored to the
target job description below.

Guidelines:
- Use strong, specific action verbs (e.g. "Engineered", "Spearheaded", "Optimised").
- Highlight and emphasise skills and experiences that directly match the job description.
- Remove or downplay experiences that are irrelevant to the role.
- Quantify achievements wherever possible (e.g. "Reduced load time by 40%").
- Keep the tone professional, concise, and ATS-friendly.
- Preserve the candidate's original section structure (Summary, Experience, Education, Skills, etc.).
- Do NOT invent qualifications or experiences the candidate does not have.

--- CURRENT RESUME ---
{resume_text}

--- TARGET JOB DESCRIPTION ---
{job_description}

Please write the full revamped resume below:
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )
    except Exception as e:
        raise RuntimeError(
            f"Failed to connect to the Gemini API. "
            f"Check your API key in the .env file.\nDetails: {e}"
        )

    if not response.text or not response.text.strip():
        raise RuntimeError("Gemini returned an empty response. Please try again.")

    return response.text.strip()
