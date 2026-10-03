from typing import List

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000,
        description="User input text"
    )


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=20,
        max_length=20000
    )


class LearningPathRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )

    days_per_week: int = Field(
        default=5,
        ge=1,
        le=7
    )

    hours_per_day: float = Field(
        default=1.0,
        gt=0,
        le=12
    )


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(
        min_length=4,
        max_length=4
    )
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    title: str
    questions: List[QuizQuestion] = Field(
        min_length=3,
        max_length=3
    )


class HealthResponse(BaseModel):
    status: str
    application: str
    version: str