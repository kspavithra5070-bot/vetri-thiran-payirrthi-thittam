from app.schemas import QuizResponse
from app.services.gemini_service import GeminiService


class QuizService:

    def __init__(
        self,
        gemini: GeminiService
    ):

        self.gemini = gemini

    async def generate(
        self,
        passage: str,
        topic: str = ""
    ) -> QuizResponse:

        data = await self.gemini.quiz(
            passage,
            topic
        )

        result = QuizResponse.model_validate(data)

        for item in result.questions:

            if item.answer not in item.options:

                raise ValueError(
                    "Quiz model returned an answer "
                    "that is not one of the options."
                )

        return result