"""Compatibility wrapper for TalentLens-AI metric card widgets."""

from ui.cards import metric_card


def metric_dashboard_card(
    title: str,
    value: str,
    subtitle: str,
    badge: str = "",
    badge_type: str = "primary",
    trend: str = "",
    trend_type: str = "primary",
    icon: str = "",
) -> None:
    """Forward arguments to the unified metric_card component in ui/cards.py.

    Args:
        title: The label text of the metric.
        value: The main display number or value.
        subtitle: Helper subtitle context description.
        badge: Optional status text to overlay.
        badge_type: Color configuration of the badge.
        trend: Unused compatibility field.
        trend_type: Unused compatibility field.
        icon: Material Symbol Outlined icon name string.
    """
    metric_card(
        title=title,
        value=value,
        subtitle=subtitle,
        badge=badge,
        badge_type=badge_type,
        icon=icon,
    )
