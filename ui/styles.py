"""Enterprise CSS design system for styling native Streamlit layouts with Stripe/Notion clean aesthetics."""


def load_css() -> str:
    """Generate global CSS stylesheet based on centralized design system tokens.

    Returns:
        Unified styling sheet content.
    """
    return """
    /* --- Centralized Design Tokens -------------------------------- */
    :root {
        --bg: #F8FAFC;
        --surface: #FFFFFF;
        --primary: #4F46E5;
        --hover: #4338CA;
        --text-primary: #111827;
        --text-secondary: #6B7280;
        --border: #E5E7EB;
        --radius: 18px;
    }

    /* --- Base Layout --------------------------------------------- */
    .stApp {
        background-color: #F8FAFC !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #111827 !important;
    }

    /* Target main view layout container */
    [data-testid="stAppViewContainer"] > section > div.block-container {
        max-width: 100% !important;
        width: 100% !important;
        padding: 32px 24px !important;
        box-sizing: border-box !important;
    }

    /* Hide default Streamlit headers, deploy buttons, and footers */
    [data-testid="stHeader"], footer, .stDeployButton {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }

    /* --- Sidebar Styling ----------------------------------------- */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #E5E7EB !important;
        width: 260px !important;
        min-width: 260px !important;
        max-width: 260px !important;
    }

    [data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        padding: 24px 16px !important;
    }

    [data-testid="stSidebar"] a {
        background-color: #FFFFFF !important;
        border-left: 3px solid transparent !important;
        padding-left: 12px !important;
        margin-bottom: 4px !important;
        display: block !important;
        text-decoration: none !important;
    }

    [data-testid="stSidebar"] a:hover {
        background-color: #EEF2FF !important;
        color: #4F46E5 !important;
    }

    .nav-active {
        background-color: #EEF2FF !important;
        border-left: 3px solid #4F46E5 !important;
        border-radius: 0 6px 6px 0 !important;
        padding-left: 12px !important;
    }

    .nav-active button {
        color: #4F46E5 !important;
        background-color: #EEF2FF !important;
        font-weight: 700 !important;
    }

    /* --- Main Container Card ------------------------------------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 18px !important;
        padding: 24px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05) !important;
        box-sizing: border-box !important;
        margin-top: 16px !important;
        margin-bottom: 16px !important;
    }

    [data-testid="stVerticalBlock"] {
        gap: 16px !important;
    }

    /* --- CTA Buttons --------------------------------------------- */
    div.stButton > button {
        background-color: #4F46E5 !important;
        color: #FFFFFF !important;
        border: 1px solid #4F46E5 !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        height: 54px !important;
        padding: 0 24px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
        transition: background-color 0.15s, border-color 0.15s !important;
        width: 100% !important;
    }

    div.stButton > button:hover {
        background-color: #4338CA !important;
        border-color: #4338CA !important;
        color: #FFFFFF !important;
    }

    /* --- Upload Cards Styling ------------------------------------- */
    [data-testid="stFileUploader"] {
        background-color: #FFFFFF !important;
        border: 2px dashed #E5E7EB !important;
        border-radius: 14px !important;
        padding: 16px !important;
        transition: border-color 0.15s ease-in-out !important;
        box-shadow: none !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #4F46E5 !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: #FFFFFF !important;
        border: none !important;
        padding: 0 !important;
    }

    /* Purple upload icon SVG path */
    [data-testid="stFileUploader"] svg {
        fill: #4F46E5 !important;
        color: #4F46E5 !important;
    }

    /* White Browse Files button with purple border & text */
    [data-testid="stFileUploader"] button,
    [data-testid="stFileUploader"] [data-testid="baseButton-secondary"],
    [data-testid="stFileUploader"] button[data-testid="baseButton-secondary"] {
        background-color: #FFFFFF !important;
        border: 1px solid #4F46E5 !important;
        color: #4F46E5 !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 6px 14px !important;
        height: auto !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
    }

    /* Hover state with light purple background */
    [data-testid="stFileUploader"] button:hover,
    [data-testid="stFileUploader"] [data-testid="baseButton-secondary"]:hover,
    [data-testid="stFileUploader"] button[data-testid="baseButton-secondary"]:hover {
        background-color: #EEF2FF !important;
        border-color: #4F46E5 !important;
        color: #4F46E5 !important;
    }

    /* Text elements inside drop uploader */
    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span {
        color: #6B7280 !important;
    }

    /* --- Uploaded File Card --------------------------------------- */
    [data-testid="stFileUploaderFile"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E5E7EB !important;
        border-radius: 10px !important;
        padding: 12px !important;
        margin-top: 8px !important;
    }

    /* --- Paste Job Description text area --------------------------- */
    [data-testid="stTextArea"] textarea {
        background-color: #FFFFFF !important;
        border: 1px solid #D1D5DB !important;
        border-radius: 12px !important;
        color: #111827 !important;
        padding: 12px !important;
        font-size: 14px !important;
        line-height: 1.5 !important;
    }

    [data-testid="stTextArea"] textarea:focus {
        border-color: #4F46E5 !important;
        box-shadow: 0 0 0 2px rgba(79, 70, 229, 0.1) !important;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: #9CA3AF !important;
    }
    """
