from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import APP_NAME, APP_VERSION
from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from models import (
    HealthResponse,
    LearningPathRequest,
    QuestionRequest,
    QuizRequest,
    TextRequest,
)
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text


# --------------------------------------------------
# Base directory
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="EduGenie - Google Gemini powered educational assistant.",
)


# --------------------------------------------------
# Static files
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)


# --------------------------------------------------
# Jinja2 templates
# --------------------------------------------------

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "app_name": APP_NAME,
            "app_version": APP_VERSION,
        },
    )


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.get(
    "/health",
    response_model=HealthResponse,
)
async def health():
    return HealthResponse(
        status="ok",
        application=APP_NAME,
        version=APP_VERSION,
    )


# --------------------------------------------------
# Q&A
# --------------------------------------------------

@app.post("/qa")
async def qa(request: QuestionRequest):
    try:
        result = answer_question(
            request.question
        )

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# --------------------------------------------------
# Explain concept
# --------------------------------------------------

@app.post("/explain")
async def explain(request: TextRequest):
    try:
        result = explain_concept(
            request.text
        )

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# --------------------------------------------------
# Generate quiz
# --------------------------------------------------

@app.post("/quiz")
async def quiz(request: QuizRequest):
    try:
        result = generate_quiz(
            request.text
        )

        return {
            "success": True,
            "result": result.model_dump(),
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# --------------------------------------------------
# Summarize text
# --------------------------------------------------

@app.post("/summarize")
async def summarize(request: TextRequest):
    try:
        result = summarize_text(
            request.text
        )

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# --------------------------------------------------
# Learning recommendations
# --------------------------------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(
    request: LearningPathRequest,
):
    try:
        result = get_learning_recommendations(
            topic=request.topic,
            level=request.level,
            days_per_week=request.days_per_week,
            hours_per_day=request.hours_per_day,
        )

        return {
            "success": True,
            "result": result,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc