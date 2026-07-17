"""Plotly visualization charts for TalentLens-AI."""

import plotly.graph_objects as go
from ui.theme import DARK_THEME, LIGHT_THEME


def _get_colors(theme: str) -> dict[str, str]:
    """Select the active theme color codes.

    Args:
        theme: Theme name ("light" or "dark").

    Returns:
        A dictionary mapping design tokens to color hex codes.
    """
    return DARK_THEME if theme == "dark" else LIGHT_THEME


def render_gauge(
    value: float,
    title: str,
    theme: str = "dark",
    grade: str = "",
) -> go.Figure:
    """Create an index score visual indicator gauge chart.

    Args:
        value: Numerical score value (0 to 100).
        title: Title of the gauge metric.
        theme: Active theme mode name ("light" or "dark").
        grade: Optional grade character overlay.

    Returns:
        A Plotly Figure object.
    """
    colors = _get_colors(theme)

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number={
                "font": {
                    "size": 36,
                    "family": "Inter",
                    "color": colors["text"],
                }
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1,
                    "tickcolor": colors["border"],
                    "tickfont": {
                        "color": colors["muted"],
                        "family": "Inter",
                        "size": 10,
                    },
                    "tickmode": "array",
                    "tickvals": [0, 25, 50, 75, 100],
                },
                "bar": {"color": colors["primary"], "thickness": 0.25},
                "bgcolor": "rgba(128, 128, 128, 0.08)",
                "borderwidth": 0,
            },
        )
    )

    if grade:
        fig.add_annotation(
            text=f"Grade {grade}",
            x=0.5,
            y=0.35,
            showarrow=False,
            font={"size": 14, "family": "Inter", "color": colors["muted"]},
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter", "color": colors["text"]},
        title={
            "text": title,
            "font": {"size": 13, "family": "Inter", "color": colors["text"]},
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
        },
        margin=dict(l=30, r=30, t=50, b=30),
        height=220,
    )
    return fig


def render_bar_chart(
    labels: list[str],
    values: list[float],
    title: str,
    theme: str = "dark",
) -> go.Figure:
    """Create a minimal horizontal comparison bar chart.

    Args:
        labels: String label names for Y axis metrics.
        values: Scores for X axis values.
        title: Title of the chart.
        theme: Active theme mode name ("light" or "dark").

    Returns:
        A Plotly Figure object.
    """
    colors = _get_colors(theme)

    fig = go.Figure(
        go.Bar(
            x=values,
            y=labels,
            orientation="h",
            marker=dict(color=colors["primary"], cornerradius=4),
            hovertemplate="%{y}: <b>%{x:.1f}</b><extra></extra>",
        )
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            range=[0, 100],
            showgrid=True,
            gridcolor=colors["border"],
            linecolor="rgba(0,0,0,0)",
            title="",
            tickfont={
                "color": colors["muted"],
                "family": "Inter",
                "size": 10,
            },
        ),
        yaxis=dict(
            showgrid=False,
            linecolor="rgba(0,0,0,0)",
            title="",
            tickfont={
                "color": colors["text"],
                "family": "Inter",
                "size": 11,
            },
        ),
        font={"family": "Inter", "color": colors["text"]},
        title={
            "text": title,
            "font": {"size": 13, "color": colors["text"], "family": "Inter"},
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
        },
        margin=dict(l=20, r=20, t=50, b=20),
        height=220,
    )
    return fig


def render_pie_chart(
    labels: list[str],
    values: list[int],
    title: str,
    theme: str = "dark",
) -> go.Figure:
    """Create a minimal donut chart displaying categorical share splits.

    Args:
        labels: Slide category name strings.
        values: Size ratios of each slice.
        title: Title of the chart.
        theme: Active theme mode name ("light" or "dark").

    Returns:
        A Plotly Figure object.
    """
    colors = _get_colors(theme)
    total = sum(values)
    match_percentage = int((values[0] / total) * 100) if total > 0 else 0

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker=dict(colors=[colors["success"], colors["danger"]]),
            textinfo="none",
            hovertemplate="%{label}: <b>%{value}</b> (%{percent})<extra></extra>",
        )
    )

    fig.add_annotation(
        text=f"{match_percentage}%",
        x=0.5,
        y=0.5,
        showarrow=False,
        font={"size": 20, "family": "Inter", "color": colors["text"], "weight": "bold"},
    )

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font={"color": colors["muted"], "family": "Inter", "size": 10},
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter", "color": colors["text"]},
        title={
            "text": title,
            "font": {"size": 13, "color": colors["text"], "family": "Inter"},
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
        },
        margin=dict(l=20, r=20, t=50, b=40),
        height=220,
    )
    return fig
