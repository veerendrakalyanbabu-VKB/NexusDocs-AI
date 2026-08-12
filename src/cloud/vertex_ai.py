"""Vertex AI Gemini integration for GCP deployments."""

from __future__ import annotations

from functools import lru_cache

from src.config import get_settings
from src.rag_pipeline import SYSTEM_PROMPT, build_prompt


@lru_cache(maxsize=1)
def create_vertex_model():
  settings = get_settings()
  import vertexai
  from vertexai.generative_models import GenerativeModel, GenerationConfig

  vertexai.init(project=settings.gcp_project, location=settings.gcp_region)
  return GenerativeModel(
      settings.vertex_model,
      system_instruction=SYSTEM_PROMPT,
      generation_config=GenerationConfig(
          temperature=0.2,
          max_output_tokens=1024,
      ),
  )


def generate_vertex_answer(question: str, context: str) -> str:
    model = create_vertex_model()
    prompt = build_prompt(question, context)
    response = model.generate_content(prompt)

    if not response.candidates:
        return "I don't know based on the provided document."

    text = response.text or ""
    return text.strip() or "I don't know based on the provided document."
