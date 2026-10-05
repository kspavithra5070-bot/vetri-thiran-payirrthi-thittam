from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings

from app.schemas import (
    ExplainRequest,
    LearnRequest,
    QARequest,
    QuizRequest,
    TextRequest,
)

from app.services.explanation_service import ExplanationService
from app.services.gemini_service import GeminiService
from app.services.local_explainer import LocalExplainer
from app.services.quiz_service import QuizService


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

settings = get_settings()

BASE_DIR = Path(__file__).resolve().parent


# ---------------------------------------------------------
# SERVICES
# ---------------------------------------------------------

gemini = GeminiService(settings)

local_explainer = LocalExplainer(settings)

explanation_service = ExplanationService(
    gemini,
    local_explainer,
)

quiz_service = QuizService(
    gemini,
)


# ---------------------------------------------------------
# FASTAPI APPLICATION
# ---------------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="EduGenie - AI-powered educational assistant",
)


# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------
# STATIC FILES
# ---------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(
        directory=str(BASE_DIR / "static"),
    ),
    name="static",
)


# ---------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates"),
)


# ---------------------------------------------------------
# INPUT CLEANING
# ---------------------------------------------------------

def clean(value: str) -> str:

    value = value.strip()

    if not value:
        raise HTTPException(
            status_code=400,
            detail="Input cannot be empty.",
        )

    if len(value) > settings.max_input_chars:
        raise HTTPException(
            status_code=413,
            detail=(
                f"Input is too long. "
                f"Maximum is {settings.max_input_chars} characters."
            ),
        )

    return value


# ---------------------------------------------------------
# HOME PAGE
# ---------------------------------------------------------

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
        },
    )
# ---------------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "gemini_configured": gemini.available,
        "local_model_enabled": settings.use_local_model,
    }


# ---------------------------------------------------------
# Q&A
# ---------------------------------------------------------

@app.post("/qa")
async def qa(
    payload: QARequest,
):

    try:

        question = clean(
            payload.question,
        )

        answer = await gemini.qa(
            question,
        )

        return {
            "result": answer,
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc


# ---------------------------------------------------------
# EXPLANATION
# ---------------------------------------------------------

@app.post("/explain")
async def explain(
    payload: ExplainRequest,
):

    try:

        topic = clean(
            payload.topic,
        )

        result = await explanation_service.explain(
            topic,
        )

        return {
            "result": result,
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc


# ---------------------------------------------------------
# QUIZ
# ---------------------------------------------------------

@app.post("/quiz")
async def quiz(
    payload: QuizRequest,
):

    try:

        text = clean(
            payload.text,
        )

        topic = payload.topic.strip()

        result = await quiz_service.generate(
            text,
            topic,
        )

        return result.model_dump()

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc


# ---------------------------------------------------------
# SUMMARY
# ---------------------------------------------------------

@app.post("/summarize")
async def summarize(
    payload: TextRequest,
):

    try:

        text = clean(
            payload.text,
        )

        result = await gemini.summary(
            text,
        )

        return {
            "result": result,
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc


# ---------------------------------------------------------
# LEARNING RECOMMENDATIONS
# ---------------------------------------------------------

@app.post("/learn/recommendations")
async def learning_recommendations(
    payload: LearnRequest,
):

    try:

        topic = clean(
            payload.topic,
        )

        result = await gemini.learning_path(
            topic,
            payload.level,
        )

        return {
            "result": result,
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc