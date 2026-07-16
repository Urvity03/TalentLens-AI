"""Visualizations module using Plotly and pandas."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from modules.models import AHRIResult, PotentialPrediction, SkillIntelligence


def create_skill_chart(skill_intelligence: SkillIntelligence) -> go.Figure:
    """Create a pie chart showing matched vs missing skills.

    Args:
        skill_intelligence: The skill intelligence results.

    Returns:
        A Plotly pie chart figure.
    """
    labels = ["Matched Skills", "Missing Skills"]
    values = [len(skill_intelligence.matched), len(skill_intelligence.missing)]
    return px.pie(names=labels, values=values, title="Skills Analysis")


def create_score_chart(
    ahri: AHRIResult,
    quality_score: float,
    prediction: PotentialPrediction,
) -> go.Figure:
    """Create a bar chart showing AHRI, Resume Quality, and Potential scores.

    Args:
        ahri: The AHRI result.
        quality_score: The resume quality score.
        prediction: The potential prediction.

    Returns:
        A Plotly bar chart figure.
    """
    metrics = ["AHRI", "Resume Quality", "Potential"]
    scores = [ahri.score, quality_score, prediction.score]
    return px.bar(
        x=metrics,
        y=scores,
        labels={"x": "Metric", "y": "Score"},
        title="Score Comparison",
    )


def create_summary_table(
    ahri: AHRIResult,
    quality_score: float,
    prediction: PotentialPrediction,
) -> pd.DataFrame:
    """Create a pandas DataFrame summary table of the candidate metrics.

    Args:
        ahri: The AHRI result.
        quality_score: The resume quality score.
        prediction: The potential prediction.

    Returns:
        A pandas DataFrame with Metric and Value columns.
    """
    data = {
        "Metric": ["AHRI", "Resume Quality", "Potential", "Grade"],
        "Value": [ahri.score, quality_score, prediction.score, ahri.grade],
    }
    return pd.DataFrame(data)
