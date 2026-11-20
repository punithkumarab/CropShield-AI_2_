"""Grounded AI Agricultural Knowledge Assistant for CropShield AI 2.0."""

from __future__ import annotations

import json
import logging
from typing import Any
import urllib.error
import urllib.request

from .knowledge_base import load_disease_knowledge

LOGGER = logging.getLogger(__name__)


class AgriculturalAssistant:
    """Retrieval-grounded agricultural decision support assistant with verified extension citations."""

    def __init__(self, ollama_endpoint: str = "http://localhost:11434"):
        self.ollama_endpoint = ollama_endpoint
        self._knowledge = load_disease_knowledge()

    def is_ollama_available(self) -> bool:
        """Check whether a local Ollama instance is actively running."""
        try:
            req = urllib.request.Request(f"{self.ollama_endpoint}/api/tags", headers={"User-Agent": "CropShield"})
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                return resp.status == 200
        except Exception:
            return False

    def retrieve_grounded_context(self, query: str) -> list[dict[str, Any]]:
        """Retrieve relevant verified disease records matching the farmer's query terms."""
        terms = [t.lower().strip() for t in query.split() if len(t) > 2]
        if not terms:
            return []

        ranked_records = []
        for class_name, record in self._knowledge.items():
            text_corpus = " ".join([
                record.get("crop", ""),
                record.get("disease", ""),
                record.get("symptoms", ""),
                record.get("distinguishing_signs", ""),
                record.get("favorable_conditions", ""),
                " ".join(record.get("immediate_steps", [])),
                " ".join(record.get("management", [])),
                " ".join(record.get("prevention", [])),
                " ".join(record.get("biological_options", [])),
            ]).lower()

            score = sum(text_corpus.count(t) for t in terms)
            if score > 0:
                ranked_records.append((score, class_name, record))

        ranked_records.sort(key=lambda x: x[0], reverse=True)
        return [item[2] for item in ranked_records[:3]]

    def answer_query(self, query: str) -> dict[str, Any]:
        """Generate an evidence-backed answer based strictly on verified agricultural extension data."""
        clean_query = query.strip()
        if not clean_query:
            return {
                "answer": "Please enter a specific question about crop symptoms, disease identification, or prevention practices.",
                "sources": [],
                "grounded": False,
            }

        matches = self.retrieve_grounded_context(clean_query)
        if not matches:
            return {
                "answer": (
                    "No verified agricultural record in the CropShield knowledge base directly matches your question. "
                    "CropShield AI does not generate speculative treatment advice. "
                    "Please consult your local Krishi Vigyan Kendra (KVK) or state agricultural extension officer."
                ),
                "sources": [],
                "grounded": False,
            }

        top_match = matches[0]
        crop = top_match.get("crop", "Crop")
        disease = top_match.get("disease", "Condition")
        symptoms = top_match.get("symptoms", "")
        management = top_match.get("management", [])
        immediate_steps = top_match.get("immediate_steps", [])
        biological = top_match.get("biological_options", [])
        source_name = top_match.get("source_name", "Agricultural Extension Source")
        source_url = top_match.get("source_url", "")
        reviewed_on = top_match.get("last_reviewed", "")

        answer_paragraphs = [
            f"**Regarding {disease} in {crop}:**",
            f"**Key Symptoms:** {symptoms}",
        ]
        if immediate_steps:
            answer_paragraphs.append("**Immediate Recommended Steps:**\n" + "\n".join(f"- {step}" for step in immediate_steps[:3]))
        if management:
            answer_paragraphs.append("**Integrated Field Management:**\n" + "\n".join(f"- {m}" for m in management[:3]))
        if biological:
            answer_paragraphs.append("**Biological / Organic Options:**\n" + "\n".join(f"- {b}" for b in biological[:2]))

        sources = [
            {
                "disease": disease,
                "crop": crop,
                "source_name": source_name,
                "source_url": source_url,
                "last_reviewed": reviewed_on,
            }
        ]

        return {
            "answer": "\n\n".join(answer_paragraphs),
            "sources": sources,
            "grounded": True,
            "disease_matched": disease,
        }
