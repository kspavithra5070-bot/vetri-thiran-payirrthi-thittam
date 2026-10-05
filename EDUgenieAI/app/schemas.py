from typing import Literal

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=12000
    )


class QARequest(TextRequest):
    question: str = Field(
        min_length=1,
        max_length=4000
    )


class ExplainRequest(TextRequest):
    topic: str = Field(
        min_length=1,
        max_length=1000
    )


class QuizRequest(TextRequest):
    topic: str = Field(
        default="",
        max_length=1000
    )


class LearnRequest(TextRequest):
    topic: str = Field(
        min_length=1,
        max_length=1000
    )

    level: Literal[
        "beginner",
        "intermediate",
        "advanced"
    ] = "beginner"


class QuizQuestion(BaseModel):
    question: str

    options: list[str] = Field(
        min_length=4,
        max_length=4
    )

    answer: str


class QuizResponse(BaseModel):
    questions: list[QuizQuestion] = Field(
        min_length=3,
        max_length=3
    )


class TextResponse(BaseModel):
    result: str