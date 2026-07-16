"""Candidate ranking logic for TalentLens-AI."""

from modules.models import AHRIResult, Resume


def rank_candidates(
    candidates: list[tuple[Resume, AHRIResult]]
) -> list[tuple[Resume, AHRIResult]]:
    """Rank candidates based on their AHRI score in descending order.

    Args:
        candidates: A list of tuples containing Resume and AHRIResult.

    Returns:
        The sorted list of tuples, highest AHRI score first.
    """
    return sorted(candidates, key=lambda item: item[1].score, reverse=True)
