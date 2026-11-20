"""Tests for grounded Agricultural Assistant service."""

from __future__ import annotations

from src.cropshield.assistant import AgriculturalAssistant


def test_assistant_retrieves_grounded_early_blight_guidance():
    assistant = AgriculturalAssistant()
    res = assistant.answer_query("How do I identify and manage early blight in tomato?")
    assert res["grounded"] is True
    assert "Early blight" in res["disease_matched"] or "Early Blight" in res["disease_matched"]
    assert len(res["sources"]) > 0
    assert "source_name" in res["sources"][0]


def test_assistant_retrieves_grounded_late_blight_guidance():
    assistant = AgriculturalAssistant()
    res = assistant.answer_query("What causes late blight water-soaked lesions?")
    assert res["grounded"] is True
    assert len(res["sources"]) > 0
    assert any("Late blight" in s["disease"] or "Late Blight" in s["disease"] for s in res["sources"])


def test_assistant_rejects_empty_query_safely():
    assistant = AgriculturalAssistant()
    res = assistant.answer_query("   ")
    assert res["grounded"] is False
    assert res["sources"] == []
    assert "Please enter a specific question" in res["answer"]


def test_assistant_rejects_ungrounded_query_without_hallucinating():
    assistant = AgriculturalAssistant()
    res = assistant.answer_query("Quantum computing crypto token price prediction")
    assert res["grounded"] is False
    assert res["sources"] == []
    assert "CropShield AI does not generate speculative treatment advice" in res["answer"]
