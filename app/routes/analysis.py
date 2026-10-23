
from urllib.parse import urlparse

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.database.history import save_analysis
from app.services.report_service import generate_report

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

ALLOWED_CONTENT_TYPES = {
    "news_article",
    "headline",
    "social_media",
    "general_claim",
}


@router.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    text: str = Form(...),
    headline: str = Form(""),
    source_url: str = Form(""),
    content_type: str = Form("general_claim"),
):
    settings = get_settings()
    errors = []

    # Clean user input.
    text = text.strip()
    headline = headline.strip()
    source_url = source_url.strip()

    # Validate the submitted text.
    if not text:
        errors.append("Please enter some text to analyze.")

    if len(text) > settings.max_text_length:
        errors.append(
            f"Your text exceeds the {settings.max_text_length:,} "
            "character limit."
        )

    # Validate the content category.
    if content_type not in ALLOWED_CONTENT_TYPES:
        errors.append("Please select a valid content type.")

    # Validate the optional headline.
    if len(headline) > 500:
        errors.append("The headline cannot exceed 500 characters.")

    # Validate the optional source URL.
    # This checks its format only; it does not fetch or verify the URL.
    if source_url:
        try:
            parsed = urlparse(source_url)

            if (
                parsed.scheme not in {"http", "https"}
                or not parsed.hostname
                or parsed.username is not None
                or parsed.password is not None
            ):
                errors.append(
                    "Enter a valid HTTP or HTTPS source URL."
                )

        except ValueError:
            errors.append("The source URL is invalid.")

    # Return the form with validation errors.
    if errors:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "app_name": settings.app_name,
                "errors": errors,
                "text": text,
                "headline": headline,
                "source_url": source_url,
                "content_type": content_type,
            },
            status_code=400,
        )

    try:
        # Generate the credibility report.
        report = await generate_report(
            text=text,
            headline=headline,
            source_url=source_url,
        )

        # Save the report in the local SQLite database.
        save_analysis(
            headline=headline,
            content_type=content_type,
            report=report,
        )

        # Display the report.
        return templates.TemplateResponse(
            request=request,
            name="results.html",
            context={
                "app_name": settings.app_name,
                "report": report,
                "headline": headline,
                "content_type": content_type,
            },
        )

    except Exception:
        # Avoid exposing API keys, provider responses, or tracebacks.
        # Detailed server-side logging can be added separately.
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "app_name": settings.app_name,
                "errors": [
                    "Analysis could not be completed. Please try again."
                ],
                "text": text,
                "headline": headline,
                "source_url": source_url,
                "content_type": content_type,
            },
            status_code=502,
        )
