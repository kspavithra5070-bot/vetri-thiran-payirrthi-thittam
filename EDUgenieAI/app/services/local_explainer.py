from app.config import Settings


class LocalExplainer:

    """
    Optional local LaMini-Flan-T5 explanation service.

    The model is loaded only when USE_LOCAL_MODEL=true.
    """

    def __init__(self, settings: Settings):

        self.settings = settings
        self._pipeline = None

    def _load(self):

        if self._pipeline is not None:
            return self._pipeline

        try:
            from transformers import pipeline

        except ImportError as exc:
            raise RuntimeError(
                "Local model support requires transformers "
                "and torch. Install requirements.txt."
            ) from exc

        self._pipeline = pipeline(
            "text2text-generation",
            model=self.settings.local_model_name,
            tokenizer=self.settings.local_model_name
        )

        return self._pipeline

    def explain(self, topic: str) -> str:

        if not self.settings.use_local_model:
            raise RuntimeError(
                "Local explanation model is disabled."
            )

        pipe = self._load()

        prompt = f"""
Explain the following educational topic
in simple language for a beginner.

Topic:
{topic}

Include:

1. Simple definition
2. Important points
3. One simple example
"""

        output = pipe(
            prompt,
            max_new_tokens=256,
            do_sample=False
        )

        return output[0]["generated_text"].strip()