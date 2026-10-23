
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database.history import (
    delete_analysis,
    get_analysis,
    list_analyses,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/history", response_class=HTMLResponse)
async def history_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={"records": list_analyses()},
    )


@router.get("/history/{analysis_id}", response_class=HTMLResponse)
async def view_saved_analysis(request: Request, analysis_id: int):
    record = get_analysis(analysis_id)

    if record is None:
        return templates.TemplateResponse(
            request=request,
            name="history.html",
            context={
                "records": list_analyses(),
                "error": "That saved report could not be found.",
            },
            status_code=404,
        )

    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={
            "app_name": "TruthLens AI",
            "report": record["report"],
            "headline": record["headline"],
            "content_type": record["content_type"],
            "saved_record": True,
        },
    )


@router.post("/history/{analysis_id}/delete")
async def remove_saved_analysis(analysis_id: int):
    delete_analysis(analysis_id)

    return RedirectResponse(
        url="/history",
        status_code=303,
    )
