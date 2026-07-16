"""Test UI rendering functions using mocks."""

from pathlib import Path
import sys
from unittest.mock import MagicMock, patch

sys.path.append(str(Path(__file__).resolve().parents[1]))


def test_ui_components():
    """Verify that all UI components render and execute without errors using streamlit mocks."""
    mock_st = MagicMock()
    mock_st.columns.return_value = (MagicMock(), MagicMock())
    mock_st.toggle.return_value = True

    # Patch streamlit in the modules to verify they call streamlit methods correctly
    with patch("ui.navbar.st", mock_st), \
         patch("ui.sidebar.st", mock_st), \
         patch("ui.cards.st", mock_st):
        
        # Test navbar
        from ui.navbar import render_navbar
        theme = render_navbar()
        assert theme in ["light", "dark"]
        assert mock_st.toggle.called
        print("[OK] navbar test passed")

        # Test sidebar
        from ui.sidebar import render_sidebar
        resume, jd, clicked = render_sidebar()
        assert mock_st.file_uploader.call_count == 2
        assert mock_st.button.called
        print("[OK] sidebar test passed")

        # Test cards
        from ui.cards import info_card, metric_card
        metric_card("Test Title", "100.0", "Test Subtitle")
        info_card("Info Title", "Some content description.")
        assert mock_st.markdown.call_count > 0
        print("[OK] cards test passed")


if __name__ == "__main__":
    print("Running UI component rendering tests...\n")
    test_ui_components()
    print("\n[SUCCESS] All UI tests passed successfully!")
