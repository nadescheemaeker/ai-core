def get_prompt(diff_text):
    return {
        "system": (
            "You are a QA engineer specialized in unit testing. Your role is to detect "
            "every new function created in the diff and generate its associated unit test."
        ),
        "user": (
            f"Identify the new functions in this diff. For each one, generate a robust unit test "
            f"(using the appropriate framework for the detected language, e.g., Pytest, Jest). "
            f"Provide only the test code:\n\n{diff_text}"
        )
    }