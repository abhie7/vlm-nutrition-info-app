from groq import Groq
from app.config.settings import settings
import asyncio
import json
from fastapi import Request


class VLMService:
    def __init__(self, request: Request):
        self.client = Groq(api_key=settings.LLM_API_KEY)
        self.logger = request.state.logger

    async def process_image(self, image_url: str, request: Request) -> dict:
        system_prompt = (
            """Extract comprehensive nutritional information..."""  # Your prompt here
        )
        self.logger.info("Starting image processing", extra={"image_url": image_url})

        for attempt in range(3):
            try:
                response = await asyncio.to_thread(
                    self.client.chat.completions.create,
                    model=settings.LLM_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": image_url},
                    ],
                    temperature=0.2,
                )
                self.logger.info(
                    "LLM response received successfully", extra={"attempt": attempt + 1}
                )
                return self._parse_response(response)
            except Exception as e:
                self.logger.error(
                    f"LLM Error (attempt {attempt + 1}): {str(e)}",
                    extra={"image_url": image_url, "attempt": attempt + 1},
                )
                await asyncio.sleep(2**attempt)
        raise RuntimeError("Failed to process image after 3 attempts")

    def _parse_response(self, response) -> dict:
        try:
            content = response.choices[0].message.content
            self.logger.debug("Successfully parsed LLM response")
            return json.loads(content)
        except Exception as e:
            self.logger.error(
                f"LLM Response parsing error: {str(e)}",
                extra={"response": str(response)},
            )
            raise ValueError("Invalid LLM response format")
