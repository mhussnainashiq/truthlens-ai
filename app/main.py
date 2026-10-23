
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.database.history import initialize_database
from app.routes.analysis import router as analysis_router
from app.routes.history import router as history_router


settings = get_settings()
templates = Jinja2Templates(directory="app/templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database when the application starts."""
    initialize_database()

    print(f"{settings.app_name} is starting...")
    print(f"Environment: {settings.app_env}")

    mode = (
        "Demo Mode"
        if settings.demo_mode or not settings.openai_api_key
        else "AI Mode"
    )
    print(f"Analysis mode: {mode}")

    yield

    print(f"{settings.app_name} has stopped.")


app = FastAPI(
    title=settings.app_name,
    description="An evidence-aware news and claim credibility checker.",
    version="1.0.0",
    lifespan=lifespan,
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

app.include_router(analysis_router)
app.include_router(history_router)


@app.get("/", response_class=HTMLResponse, name="home")
async def home(request: Request):
    """Display the main analysis page."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.app_name,
            "errors": [],
            "text": "",
            "headline": "",
            "source_url": "",
            "content_type": "general_claim",
        },
    )


@app.get("/health", name="health_check")
async def health_check():
    """Return a JSON health-check response."""
    mode = (
        "demo"
        if settings.demo_mode or not settings.openai_api_key
        else "ai"
    )

    return {
        "status": "ok",
        "application": settings.app_name,
        "mode": mode,
    }


@app.get("/status", response_class=HTMLResponse, name="system_status")
async def system_status(request: Request):
    """Display the System Status HTML page."""
    mode = (
        "Demo Mode"
        if settings.demo_mode or not settings.openai_api_key
        else "AI Mode"
    )

    return templates.TemplateResponse(
        request=request,
        name="status.html",
        context={
            "app_name": settings.app_name,
            "mode": mode,
            "database_status": "Initialized",
            "analysis_status": "Available",
        },
    )
