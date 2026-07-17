"""Test suite for Plotly charts component module."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import plotly.graph_objects as go
from ui.charts import render_bar_chart, render_gauge, render_pie_chart
from ui.theme import DARK_THEME, LIGHT_THEME


def test_render_gauge():
    """Verify gauge chart layout properties for both light and dark themes."""
    # Test light theme
    fig_light = render_gauge(75.5, "Candidate Readiness", theme="light")
    assert isinstance(fig_light, go.Figure)
    assert fig_light.layout.font.family == "Inter"
    assert fig_light.layout.font.color == LIGHT_THEME["text"]
    assert fig_light.layout.paper_bgcolor == "rgba(0,0,0,0)"
    assert fig_light.data[0].type == "indicator"
    assert fig_light.data[0].value == 75.5
    assert fig_light.data[0].gauge.bar.color == LIGHT_THEME["primary"]

    # Test dark theme
    fig_dark = render_gauge(75.5, "Candidate Readiness", theme="dark")
    assert isinstance(fig_dark, go.Figure)
    assert fig_dark.layout.font.color == DARK_THEME["text"]
    assert fig_dark.data[0].gauge.bar.color == DARK_THEME["primary"]

    print("[OK] Render gauge tests (light/dark) passed")


def test_render_bar_chart():
    """Verify bar chart layout properties for both light and dark themes."""
    labels = ["AHRI", "Resume Quality", "Potential"]
    values = [80.0, 90.0, 85.0]

    # Test light theme
    fig_light = render_bar_chart(labels, values, "Overall Metrics", theme="light")
    assert isinstance(fig_light, go.Figure)
    assert fig_light.layout.font.family == "Inter"
    assert fig_light.layout.font.color == LIGHT_THEME["text"]
    assert fig_light.layout.paper_bgcolor == "rgba(0,0,0,0)"
    assert fig_light.data[0].type == "bar"
    assert fig_light.data[0].marker.color == LIGHT_THEME["primary"]

    # Test dark theme
    fig_dark = render_bar_chart(labels, values, "Overall Metrics", theme="dark")
    assert isinstance(fig_dark, go.Figure)
    assert fig_dark.layout.font.color == DARK_THEME["text"]
    assert fig_dark.data[0].marker.color == DARK_THEME["primary"]

    print("[OK] Render bar chart tests (light/dark) passed")


def test_render_pie_chart():
    """Verify pie donut chart layout properties for both light and dark themes."""
    labels = ["Matched", "Missing"]
    values = [15, 5]

    # Test light theme
    fig_light = render_pie_chart(labels, values, "Skills Match", theme="light")
    assert isinstance(fig_light, go.Figure)
    assert fig_light.layout.font.family == "Inter"
    assert fig_light.layout.font.color == LIGHT_THEME["text"]
    assert fig_light.layout.paper_bgcolor == "rgba(0,0,0,0)"
    assert fig_light.data[0].type == "pie"
    assert fig_light.data[0].hole == 0.45
    # The donut segments should match the light theme success/danger colors
    assert list(fig_light.layout.piecolorway) == [
        LIGHT_THEME["success"],
        LIGHT_THEME["danger"],
    ]

    # Test dark theme
    fig_dark = render_pie_chart(labels, values, "Skills Match", theme="dark")
    assert isinstance(fig_dark, go.Figure)
    assert fig_dark.layout.font.color == DARK_THEME["text"]
    assert list(fig_dark.layout.piecolorway) == [
        DARK_THEME["success"],
        DARK_THEME["danger"],
    ]

    print("[OK] Render pie chart tests (light/dark) passed")


if __name__ == "__main__":
    print("Running charts UI tests...\n")
    test_render_gauge()
    test_render_bar_chart()
    test_render_pie_chart()
    print("\n[SUCCESS] All charts tests passed successfully!")
