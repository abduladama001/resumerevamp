ResumeForge — AI-Powered Resume Revamp System
A beginner-friendly Python desktop web app that reads a PDF resume, compares it against a job description, and uses Google Gemini AI to generate a tailored, professional rewrite.
Built with Python, Streamlit, PyMuPDF, and the google-genai package.

Project Structure
resumerevamp/
├── app.py              # Main Streamlit UI — run this file
├── extractor.py        # PDF text extraction (PyMuPDF)
├── revamper.py         # Gemini AI rewrite logic (google-genai)
├── scorer.py           # Keyword match scoring (optional expansion)
├── exporter.py         # PDF export (optional expansion)
├── requirements.txt    # All dependencies
├── .env                # Your API key (you create this — do NOT share it)
└── .env.example        # Template showing what .env should look like

Setup Instructions

Clone or download the project

bashgit clone <your-repo-url>
cd resumerevamp

Create a virtual environment (recommended)

bashpython -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

Install dependencies

bashpip install -r requirements.txt

Get your free Gemini API key
Go to https://aistudio.google.com
Sign in with a Google account
Click "Get API key" → "Create API key"
Copy the key
Create your .env file
Create a file named .env in the project root (same folder as app.py):

GEMINI_API_KEY=paste_your_key_here

⚠️ Never share your .env file or commit it to GitHub. Add it to .gitignore.


Run the app

bashstreamlit run app.py
The app will open automatically in your browser at http://localhost:8501.

How to Use

Upload your resume — click the file uploader and select a PDF resume
Paste a job description — copy a job post and paste it into the text area
Click "Revamp My Resume" — the app will:

Show your keyword match score (how well your current resume matches the job)
Display matched and missing keywords
Generate an AI-rewritten resume tailored to the job
Let you download the result as a PDF




Requirements

Python 3.10 or higher
A free Google AI Studio account (for the Gemini API key)
A text-based PDF resume (scanned image PDFs are not supported)


Troubleshooting
ProblemSolutionGEMINI_API_KEY not foundMake sure your .env file exists and has the correct keyNo text extracted from PDFYour PDF may be scanned/image-based. Use a text-based PDFModuleNotFoundErrorRun pip install -r requirements.txt againApp won't startMake sure you're in the right folder and virtual env is active

Built With

Streamlit — UI framework
PyMuPDF — PDF text extraction
google-genai — Gemini API client
fpdf2 — PDF export
python-dotenv — API key management
