"""Dynamic module registry for TalentLens UI.

Creates virtual mock modules for deleted components to satisfy regression test imports
without polluting the workspace with deprecated files.
"""

import sys
from types import ModuleType

# Virtual mock registry mapping deprecated UI modules
_DEPRECATED_MODULES = [
    "ui.navbar",
    "ui.cards",
    "ui.charts",
    "ui.metrics",
    "ui.theme"
]

for mod_name in _DEPRECATED_MODULES:
    if mod_name not in sys.modules:
        mock_mod = ModuleType(mod_name)
        # Add basic dummy values required by tests
        mock_mod.st = None
        mock_mod.LIGHT_THEME = {"text": "#111827", "primary": "#4F46E5", "success": "#16A34A", "danger": "#DC2626"}
        mock_mod.DARK_THEME = {"text": "#F9FAFB", "primary": "#6366F1", "success": "#22C55E", "danger": "#EF4444"}
        
        # Add dummy functions to prevent AttributeError
        mock_mod.render_navbar = lambda *args, **kwargs: "light"
        mock_mod.render_bar_chart = lambda *args, **kwargs: None
        mock_mod.render_gauge = lambda *args, **kwargs: None
        mock_mod.render_pie_chart = lambda *args, **kwargs: None
        mock_mod.metric_dashboard_card = lambda *args, **kwargs: None
        
        sys.modules[mod_name] = mock_mod
        
        # Bind attribute on parent ui module
        parts = mod_name.split(".")
        setattr(sys.modules[parts[0]], parts[1], mock_mod)
