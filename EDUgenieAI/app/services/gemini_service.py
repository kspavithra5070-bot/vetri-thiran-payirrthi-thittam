import json
from typing import Any

from app.config import Settings


class GeminiService:

    def __init__(self, settings: Settings):
        self.settings = settings
        self.client = None

        if settings.gemini_api_key:

            try:
                from google import genai

            except ImportError as exc:
                raise RuntimeError(
                    "google-genai is not installed. "
                    "Run: pip install -r requirements.txt"
                ) from exc

            self.client = genai.Client(
                api_key=settings.gemini_api_key
            )

    @property
    def available(self) -> bool:
        return self.client is not None

    async def generate(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
        json_schema: dict | None = None
    ) -> str:

        if not self.client:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Add it to the .env file."
            )

        from google.genai import types

        config_kwargs: dict[str, Any] = {
            "temperature": 0.4,
            "max_output_tokens": 2048,
        }

        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction

        if json_schema:
            config_kwargs["response_mime_type"] = "application/json"
            config_kwargs["response_schema"] = json_schema

        response = await self.client.aio.models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                **config_kwargs
            ),
        )

        text = response.text

        if not text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return text.strip()

    # ---------------------------------------------------------
    # QUESTION ANSWERING
    # ---------------------------------------------------------

    async def qa(self, question: str) -> str:

        prompt = f"""
Answer the following educational question clearly
and accurately.

Question:
{question}
"""

        return await self.generate(
            prompt,
            system_instruction=(
                "You are EduGenie, a concise educational "
                "assistant. Explain concepts at an appropriate "
                "student level and avoid unsupported claims."
            ),
        )

    # ---------------------------------------------------------
    # SUMMARY
    # ---------------------------------------------------------

    async def summary(self, text: str) -> str:

        prompt = f"""
Summarize the following educational passage.

Keep the important facts.
Remove unnecessary repetition.
Make the result easy for a student to revise.

Educational passage:
{text}
"""

        return await self.generate(
            prompt,
            system_instruction=(
                "Return a concise, study-friendly summary. "
                "Use short paragraphs or bullet points when useful."
            ),
        )

    # ---------------------------------------------------------
    # LEARNING PATH
    # ---------------------------------------------------------

    async def learning_path(
        self,
        topic: str,
        level: str
    ) -> str:

        prompt = f"""
Create a structured learning path for:

Topic: {topic}
Student level: {level}

Include:

1. Prerequisites
2. Basic concepts
3. Intermediate concepts
4. Advanced concepts
5. Suggested order of learning
6. Approximate study time
7. Practice activities
8. Suggested resource types
9. Small projects or exercises

Make the plan practical for a student.
"""

        return await self.generate(
            prompt,
            system_instruction=(
                "You are a learning-path designer. "
                "Create realistic, actionable and logically "
                "sequenced study plans."
            ),
        )

    # ---------------------------------------------------------
    # QUIZ
    # ---------------------------------------------------------

    async def quiz(
        self,
        passage: str,
        topic: str = ""
    ) -> dict:

        schema = {
            "type": "OBJECT",
            "properties": {
                "questions": {
                    "type": "ARRAY",
                    "minItems": 3,
                    "maxItems": 3,

                    "items": {
                        "type": "OBJECT",

                        "properties": {
                            "question": {
                                "type": "STRING"
                            },

                            "options": {
                                "type": "ARRAY",
                                "minItems": 4,
                                "maxItems": 4,

                                "items": {
                                    "type": "STRING"
                                }
                            },

                            "answer": {
                                "type": "STRING"
                            }
                        },

                        "required": [
                            "question",
                            "options",
                            "answer"
                        ]
                    }
                }
            },

            "required": [
                "questions"
            ]
        }

        prompt = f"""
Generate exactly THREE multiple-choice questions.

Topic:
{topic or "General"}

Use only the educational material provided below.

Rules:

- Exactly 3 questions
- Exactly 4 options for every question
- Exactly one correct answer
- The answer must exactly match one option
- Questions must be relevant to the supplied material
- Options should be plausible

Educational material:

{passage}
"""

        raw = await self.generate(
            prompt,
            system_instruction=(
                "You generate educational multiple-choice "
                "questions for students."
            ),
            json_schema=schema,
        )

        try:
            return json.loads(raw)

        except json.JSONDecodeError as exc:
            raise RuntimeError(
                "Gemini returned invalid JSON for the quiz."
            ) from exc