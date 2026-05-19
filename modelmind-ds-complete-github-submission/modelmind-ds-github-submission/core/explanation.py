def generate_explanation(task_type: str, recommendations: list[dict], baseline_result: dict) -> str:
    """Generate a plain-language explanation for the workflow decision."""
    lines = []

    lines.append(f"The dataset was routed as a **{task_type}** problem.")

    if recommendations:
        lines.append("Recommended model family:")
        for item in recommendations:
            lines.append(f"- {item['model']}: {item['reason']}")

    lines.append(
        f"The baseline experiment selected **{baseline_result.get('best_model')}** "
        f"based on **{baseline_result.get('metric_name')} = {baseline_result.get('metric_value')}**."
    )

    lines.append(f"Reasoning note: {baseline_result.get('note')}")

    lines.append(
        "In an industrial setting, this output should be reviewed by a domain expert before deployment."
    )

    return "\n".join(lines)
