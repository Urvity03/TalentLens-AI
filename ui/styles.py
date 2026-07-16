"""Premium CSS Stylesheet definitions for the Streamlit frontend."""


def load_css() -> str:
    """Return a custom CSS string to style the Streamlit interface.

    Includes Google Fonts, rounded cards, soft shadows, glassmorphism classes,
    hover animations, nice buttons, customized metrics, scrollbar, and sidebar
    styles.

    Returns:
        A stylesheet string containing all CSS classes.
    """
    return """
    /* --- Google Font --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* --- Rounded Cards & Soft Shadows --- */
    .premium-card {
        background-color: var(--card-bg, #FFFFFF);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }

    .premium-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -4px rgba(0, 0, 0, 0.08);
    }

    /* --- Glassmorphism Effect --- */
    .glass-card {
        background: rgba(255, 255, 255, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        margin-bottom: 1rem;
    }

    /* --- Button Styling --- */
    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0.6rem 1.8rem;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: #FFFFFF !important;
        border: none;
        box-shadow: 0 4px 14px 0 rgba(99, 102, 241, 0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        width: auto;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 20px 0 rgba(99, 102, 241, 0.4);
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        color: #FFFFFF !important;
    }

    div.stButton > button:active {
        transform: translateY(1px);
    }

    /* --- Streamlit Metric Override --- */
    [data-testid="stMetric"] {
        background-color: var(--card-bg, #FFFFFF);
        border-radius: 14px;
        border: 1px solid rgba(226, 232, 240, 0.8);
        padding: 1rem 1.25rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-1px);
    }

    /* --- Custom Scrollbar --- */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: transparent;
    }

    ::-webkit-scrollbar-thumb {
        background: #CBD5E1;
        border-radius: 9999px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #94A3B8;
    }

    /* --- Sidebar Premium Styling --- */
    [data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p {
        color: #F1F5F9 !important;
    }

    /* --- Responsive Spacing and General Overrides --- */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1200px !important;
    }
    """
