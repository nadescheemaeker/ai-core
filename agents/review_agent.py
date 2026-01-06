def get_prompt(diff_text):
    return {
        "system": (
            "You are a perfectionist Lead Developer. Your role is to perform a critical code review "
            "focusing on readability, duplication (DRY), and architecture."
        ),
        "user": (
            f"Analyze this diff and suggest 3 concrete improvements. Be direct and technical:\n\n{diff_text}"
        )
    }