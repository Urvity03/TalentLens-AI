"""Test the visualizations module."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import plotly.graph_objects as go
from modules.models import AHRIResult, PotentialPrediction, SkillIntelligence
from modules.visualizations import (
    create_score_chart,
    create_skill_chart,
    create_summary_table,
)


def test_visualizations():
    """Test visualization generation functions."""
    # Setup mock data
    si = SkillIntelligence(matched=["Python", "SQL"], missing=["Docker"], match_percentage=66.67)
    ahri = AHRIResult(score=82.5, grade="A")
    quality_score = 90.0
    prediction = PotentialPrediction(score=85.0, level="Excellent")

    # 1. Test create_skill_chart
    fig_skill = create_skill_chart(si)
    assert isinstance(fig_skill, go.Figure)
    # Verify title
    assert fig_skill.layout.title.text == "Skills Analysis"
    print("[OK] Skill chart test passed")

    # 2. Test create_score_chart
    fig_score = create_score_chart(ahri, quality_score, prediction)
    assert isinstance(fig_score, go.Figure)
    # Verify title
    assert fig_score.layout.title.text == "Score Comparison"
    print("[OK] Score chart test passed")

    # 3. Test create_summary_table
    df_summary = create_summary_table(ahri, quality_score, prediction)
    assert isinstance(df_summary, pd.DataFrame)
    assert list(df_summary.columns) == ["Metric", "Value"]
    assert len(df_summary) == 4
    
    # Verify row values
    assert df_summary.iloc[0]["Metric"] == "AHRI"
    assert df_summary.iloc[0]["Value"] == 82.5

    assert df_summary.iloc[1]["Metric"] == "Resume Quality"
    assert df_summary.iloc[1]["Value"] == 90.0

    assert df_summary.iloc[2]["Metric"] == "Potential"
    assert df_summary.iloc[2]["Value"] == 85.0

    assert df_summary.iloc[3]["Metric"] == "Grade"
    assert df_summary.iloc[3]["Value"] == "A"
    print("[OK] Summary table test passed")


if __name__ == "__main__":
    print("Running visualizations module tests...\n")
    test_visualizations()
    print("\n[SUCCESS] All visualizations tests passed successfully!")
