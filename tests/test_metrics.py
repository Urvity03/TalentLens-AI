"""Test suite for metrics UI rendering."""

from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

sys.path.append(str(Path(__file__).resolve().parents[1]))

from ui.metrics import metric_dashboard_card


def test_metric_dashboard_card():
    """Verify that metric_dashboard_card compiles and delegates to st.markdown correctly."""
    mock_st = MagicMock()

    with patch("ui.metrics.st", mock_st):
        # 1. Test rendering with badge
        metric_dashboard_card(
            title="AI Hiring Readiness",
            value="91",
            subtitle="Outstanding",
            badge="🟢 High",
        )
        assert mock_st.markdown.call_count == 1
        call_args = mock_st.markdown.call_args[0][0]
        assert "AI Hiring Readiness" in call_args
        assert "91" in call_args
        assert "Outstanding" in call_args
        assert "🟢 High" in call_args
        print("[OK] Metric card with badge passed")

        # Reset mock
        mock_st.reset_mock()

        # 2. Test rendering without badge
        metric_dashboard_card(
            title="Skill Matching",
            value="85%",
            subtitle="Partial Match",
        )
        assert mock_st.markdown.call_count == 1
        call_args_no_badge = mock_st.markdown.call_args[0][0]
        assert "Skill Matching" in call_args_no_badge
        assert "85%" in call_args_no_badge
        assert "Partial Match" in call_args_no_badge
        # Should not contain absolute badge position styling structure
        assert "position: absolute;" not in call_args_no_badge
        print("[OK] Metric card without badge passed")


if __name__ == "__main__":
    print("Running metrics UI tests...\n")
    test_metric_dashboard_card()
    print("\n[SUCCESS] All metrics tests passed successfully!")
