def get_prompt(diff_text):
    return {
        "system": (
            "You are a Technical Writer. Your goal is to make code changes "
            "understandable for humans (developers and product owners)."
        ),
        "user": (
            f"Write a changelog (release notes) for these changes. "
            f"Include a 'Summary' section and a detailed list of technical impacts:\n\n{diff_text}"
        )
    }