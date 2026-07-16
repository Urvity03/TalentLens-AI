"""Career roadmap generation based on skill gaps."""

from modules.models import CareerRoadmap, SkillIntelligence

_CUSTOM_RECOMMENDATIONS = {
    "python": "Master Python fundamentals, object-oriented programming, and advanced concepts.",
    "sql": "Learn SQL syntax, complex queries, joins, and database design principles.",
    "tensorflow": "Build and train neural networks using TensorFlow and Keras API.",
    "pytorch": "Master PyTorch tensors, autograd, and build custom deep learning models.",
    "docker": "Understand containerization concepts, write Dockerfiles, and use Docker Compose.",
    "aws": "Learn core AWS services including EC2, S3, RDS, and Lambda for cloud applications.",
    "nlp": "Study natural language processing techniques, tokenization, embeddings, and transformers.",
    "machine learning": "Understand supervised/unsupervised machine learning algorithms using scikit-learn.",
    "git": "Master Git version control, branching, merging, and GitHub workflows.",
}


def generate_career_roadmap(
    skill_intelligence: SkillIntelligence,
) -> CareerRoadmap:
    """Generate a learning roadmap based on missing skills.

    Args:
        skill_intelligence: The computed skill intelligence match results.

    Returns:
        A CareerRoadmap containing the learning steps.
    """
    if not skill_intelligence.missing:
        return CareerRoadmap(
            steps=[
                "Continue building real-world projects and keep your skills up to date."
            ]
        )

    steps: list[str] = []
    for skill in skill_intelligence.missing:
        skill_lower = skill.lower()
        if skill_lower in _CUSTOM_RECOMMENDATIONS:
            steps.append(_CUSTOM_RECOMMENDATIONS[skill_lower])
        else:
            steps.append(f"Learn {skill} and complete at least one practical project.")

    return CareerRoadmap(steps=steps)
