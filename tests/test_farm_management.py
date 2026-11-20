"""Tests for farm, plot, and expert review management."""

from __future__ import annotations

import pytest
from src.cropshield import history


def test_farm_creation_and_listing(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "DB_PATH", tmp_path / "farms_test.db")
    farm_id = history.create_farm(
        name="Green Valley Organic",
        location="Doddaballapura, Karnataka",
        total_acres=12.5,
        primary_crop="Tomato",
    )
    assert isinstance(farm_id, int)
    assert farm_id > 0

    farms = history.list_farms()
    assert len(farms) == 1
    assert farms[0]["name"] == "Green Valley Organic"
    assert farms[0]["total_acres"] == pytest.approx(12.5)


def test_farm_creation_rejects_empty_name(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "DB_PATH", tmp_path / "farms_test.db")
    with pytest.raises(ValueError, match="Farm name cannot be empty"):
        history.create_farm(name="   ", location="Zone 1", total_acres=5.0)


def test_plot_lifecycle_and_status_updates(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "DB_PATH", tmp_path / "farms_test.db")
    farm_id = history.create_farm("Cauvery Agro", "Mandya", 20.0, "Tomato")
    plot_id = history.create_plot(
        farm_id=farm_id,
        name="Sector 3 - Arka Rakshak",
        crop_variety="Arka Rakshak F1",
        planting_date="2026-09-15",
        soil_type="Red Sandy Loam",
        irrigation_type="Drip Irrigation",
        health_status="Healthy",
    )
    assert plot_id > 0

    plots = history.list_plots(farm_id=farm_id)
    assert len(plots) == 1
    assert plots[0]["name"] == "Sector 3 - Arka Rakshak"
    assert plots[0]["health_status"] == "Healthy"

    history.update_plot_status(plot_id=plot_id, health_status="Infected")
    updated = history.list_plots(farm_id=farm_id)
    assert updated[0]["health_status"] == "Infected"


def test_expert_review_workflow(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "DB_PATH", tmp_path / "farms_test.db")
    review_id = history.create_expert_review(
        prediction_id=101,
        plant_id=None,
        agronomist_name="Dr. Sunita Rao",
        status="Verified",
        expert_notes="Confirmed early Alternaria conidiophores.",
        recommended_action="Apply Trichoderma harzianum soil drench.",
    )
    assert review_id > 0

    reviews = history.list_expert_reviews()
    assert len(reviews) == 1
    assert reviews[0]["agronomist_name"] == "Dr. Sunita Rao"
    assert reviews[0]["status"] == "Verified"
    assert "Alternaria" in reviews[0]["expert_notes"]
