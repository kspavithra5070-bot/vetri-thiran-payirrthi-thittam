from app.services.gemini_service import GeminiService
from app.services.local_explainer import LocalExplainer


class ExplanationService:

    def __init__(
        self,
        gemini: GeminiService,
        local: LocalExplainer
    ):

        self.gemini = gemini
        self.local = local

    async def explain(self, topic: str) -> str:

        # Try local LaMini model first
        if self.local.settings.use_local_model:

            try:
                return self.local.explain(topic)

            except Exception:
                # Fall back to Gemini
                pass

        # Gemini explanation
        prompt = f"""
Explain the topic "{topic}" for a beginner.

Include:

1. Simple definition
2. 3 to 5 important points
3. One easy example
4. Why the concept is useful
"""

        return await self.gemini.generate(
            prompt,

            system_instruction=(
                "You are EduGenie's explanation module. "
                "Prioritize clarity, correctness and "
                "simple language."
            )
        )