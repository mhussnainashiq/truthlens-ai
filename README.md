# TruthLens AI 

**An AI-assisted news and claim credibility checker built with Python and FastAPI.**

TruthLens AI helps users examine news articles, headlines, social media posts, and general claims. It identifies potentially sensational wording, extracts statements for review, searches the web for related sources, and organizes findings into a structured credibility report.

> **Important:** Search results are leads for further investigation, not proof of a claim's truth or falsity. The current implementation does not independently establish factual accuracy. Reports may return “Insufficient Evidence” when claims have not been independently verified.

##  Features

- **Claim extraction:** Identify candidate statements from submitted text.
- **Web source discovery:** Search for potentially relevant sources using the Tavily API.
- **AI integration:** Optional OpenAI API integration for structured analysis.
- **Bias indicators:** Highlight language patterns that may warrant closer review.
- **Red-flag detection:** Identify sensational wording, percentages, and references to research that need checking.
- **Credibility reports:** Present assessments, evidence limitations, and recommended checks.
- **Analysis history:** Save, view, and delete previous reports using SQLite.
- **System status:** View application status and access API documentation.
- **Demo mode:** Run without API credentials using clearly labeled demo reports.
- **Automated tests:** Validate models, analysis behavior, and application routes.

##  Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | Web framework and HTTP routes |
| Jinja2 | HTML templates |
| Pydantic | Data validation and report models |
| OpenAI API | Optional AI-assisted analysis |
| Tavily API | Web search and source discovery |
| SQLite | Local analysis history |
| HTML, CSS, JavaScript | User interface and interactions |
| pytest | Automated testing |
| httpx | HTTP requests to external APIs |

```
*The tree represents the intended project layout; optional or newly added files may differ in your local copy.*

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or a compatible version supported by your installed dependencies
- pip
- Git
- Optional API keys for OpenAI and Tavily

### 1. Clone the repository

```bash
git clone https://github.com/mhussnainashiq/truthlens-ai.git
cd truthlens-ai
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, consult the official Python documentation for your environment's execution-policy options. You can also run the environment's Python executable directly.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a local `.env` file in the project root by copying `.env.example`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and configure the settings you need:

```dotenv
APP_NAME=TruthLens AI
APP_ENV=development
DATABASE_PATH=truthlens_history.db

OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini

TAVILY_API_KEY=

MAX_TEXT_LENGTH=15000
REQUEST_TIMEOUT_SECONDS=20
DEMO_MODE=true
```

- Add your own OpenAI API key if you want to enable the configured OpenAI integration.
- Add your own Tavily API key to enable web searches.
- Keep `DEMO_MODE=true` for demo behavior. Review the application's configuration and analyzer logic before switching modes.
- Never commit `.env` or expose API keys in source code, screenshots, or public logs.

API access may require an account and may incur usage charges.

### 5. Run the application

From the project root:

```powershell
python -m uvicorn app.main:app --reload
```

##  Running Tests

Run the test suite from the project root:

```powershell
python -m pytest -v
```

Tests cover report-model validation, claim extraction, red-flag detection, demo-report behavior, and selected application routes.

##  How It Works

1. The user submits a news article, headline, social media post, or claim.
2. The application validates the submitted input.
3. Candidate statements are extracted for further review.
4. The analyzer generates a structured report using demo behavior or the configured AI integration.
5. Tavily can retrieve potentially relevant web search results.
6. Retrieved results are presented as related sources, not automatically classified as supporting or contradicting evidence.
7. The report is saved to SQLite and displayed to the user.

##  Current Limitations

- Web search results are not independently verified evidence.
- The current report pipeline conservatively marks claims as unverified and the overall assessment as insufficient evidence.
- Sensational wording and other red flags are review prompts, not proof of misinformation.
- AI-generated analysis can be incomplete or incorrect.
- Source credibility, publication context, original documents, dates, and corroboration require human review.
- The application is a development project, not a replacement for professional fact-checking or editorial judgment.

##  Security Notes

- Keep API keys in `.env`; never publish secrets.
- Do not commit virtual environments, local databases, or private configuration files.
- Treat submitted text and external search content as untrusted input.
- Before deploying publicly, review rate limiting, request validation, output escaping, logging, and external-service error handling.
- If adding URL fetching, implement appropriate SSRF protections and avoid unrestricted access to internal or private network addresses.

## 🗺️ Future Improvements

- Evidence evaluation using explicit supporting and contradicting source criteria
- Source credibility and publication-date analysis
- Claim-level citations with traceable evidence
- More robust bias and misleading-language analysis
- Improved report export and filtering
- Deployment with production configuration, logging, and rate limiting
- Expanded automated tests and user-facing documentation

##  Author

**Muhammad Husnain Ashiq**

- GitHub: [@mhussnainashiq](https://github.com/mhussnainashiq)
- Project: [TruthLens AI](https://github.com/mhussnainashiq/truthlens-ai)

## 📄License

No license has been specified yet. Add a license file if you want to explicitly grant others permission to use, modify, and distribute this project.
