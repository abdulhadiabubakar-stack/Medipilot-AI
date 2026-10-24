# MediPilot AI

MediPilot AI is a Streamlit prototype for healthcare operations in Gombe, Nigeria. It demonstrates simulated emergency workflows, facility discovery, appointment preparation, reminders, and an activity log.

**Demo only:** The app does not diagnose or prescribe, place calls, contact facilities or emergency contacts, access real GPS, send messages, or book real appointments.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Optional Gemini smoke check

`test_gemma.py` makes a live request to Google's Gemini API. To use it, create `.streamlit/secrets.toml` locally with your own key:

```toml
GEMINI_API_KEY = "your-api-key"
```

Then run `python test_gemma.py`. Keep this secrets file private; it is excluded from Git.
