"""Premium reusable Plotly chart components for TalentLens-AI."""

import plotly.express as px
import plotly.graph_objects as go

from ui.theme import DARK_THEME, LIGHT_THEME


def _get_theme_colors(theme: str) -> dict[str, any]:
    """Helper to select active theme colors and layout adjustments.

    Args:
        theme: Theme name ("light" or "dark").

    Returns:
        Dictionary containing theme color values.
    """
    t = DARK_THEME if theme == "dark" else LIGHT_THEME
    is_dark = theme == "dark"

    return {
        "font_color": t["text"],
        "axis_color": "rgba(255, 255, 255, 0.2)" if is_dark else "rgba(0, 0, 0, 0.15)",
        "grid_color": "rgba(255, 255, 255, 0.08)" if is_dark else "rgba(0, 0, 0, 0.06)",
        "palette": [
            t["primary"],
            t["accent"],
            t["success"],
            t["warning"],
            t["danger"],
        ],
    }


def render_gauge(value: float, title: str, theme: str = "light") -> go.Figure:
    """Create a circular gauge chart for a score.

    Args:
        value: Score value between 0 and 100.
        title: Title of the gauge.
        theme: Theme mode to render ("light" or "dark").

    Returns:
        A Plotly Figure object.
    """
    colors = _get_theme_colors(theme)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title, "font": {"size": 16, "family": "Inter", "color": colors["font_color"]}},
            number={"font": {"color": colors["font_color"]}},
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": colors["axis_color"],
                    "tickfont": {"color": colors["font_color"]},
                },
                "bar": {"color": colors["palette"][0], "thickness": 0.8},
                "bgcolor": colors["grid_color"],
                "borderwidth": 0,
            },
        )
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter", "color": colors["font_color"]},
        margin=dict(l=20, r=20, t=50, b=20),
        height=240,
    )
    return fig


def render_bar_chart(
    labels: list[str],
    values: list[float],
    title: str,
    theme: str = "light",
) -> go.Figure:
    """Create a responsive bar chart with rounded styling and minimal grid.

    Args:
        labels: List of label names for X axis.
        values: List of numeric values for Y axis.
        title: Title of the chart.
        theme: Theme mode to render ("light" or "dark").

    Returns:
        A Plotly Figure object.
    """
    colors = _get_theme_colors(theme)
    fig = px.bar(
        x=labels,
        y=values,
        title=title,
        color_discrete_sequence=[colors["palette"][0]],
    )
    fig.update_traces(marker_cornerradius=8)
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            showgrid=False,
            linecolor=colors["axis_color"],
            title="",
            tickfont={"color": colors["font_color"]},
        ),
        yaxis=dict(
            gridcolor=colors["grid_color"],
            linecolor=colors["axis_color"],
            title="",
            tickfont={"color": colors["font_color"]},
        ),
        font={"family": "Inter", "color": colors["font_color"]},
        title_font={"color": colors["font_color"]},
        margin=dict(l=20, r=20, t=40, b=20),
        height=280,
    )
    return fig


def render_pie_chart(
    labels: list[str],
    values: list[int],
    title: str,
    theme: str = "light",
) -> go.Figure:
    """Create a donut-style pie chart using the theme's color palette.

    Args:
        labels: List of slice label names.
        values: List of slice sizes.
        title: Title of the chart.
        theme: Theme mode to render ("light" or "dark").

    Returns:
        A Plotly Figure object.
    """
    colors = _get_theme_colors(theme)
    fig = px.pie(
        names=labels,
        values=values,
        title=title,
        hole=0.45,
        color_discrete_sequence=colors["palette"],
    )
    fig.update_traces(
        textinfo="percent+label",
        textposition="inside",
        insidetextfont={"color": "#FFFFFF"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter", "color": colors["font_color"]},
        title_font={"color": colors["font_color"]},
        legend={"font": {"color": colors["font_color"]}},
        margin=dict(l=20, r=20, t=40, b=20),
        height=280,
    )
    return fig
