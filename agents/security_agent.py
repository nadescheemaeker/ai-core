def get_prompt(diff_text):
    return {
        "system": (
            "You are a cybersecurity expert. Your role is to track logical vulnerabilities, "
            "injections, and accidental exposure of sensitive data."
        ),
        "user": (
            f"Scan this diff for any security vulnerabilities. If you find any, explain "
            f"the risk and provide the fix:\n\n{diff_text}"
        )
    }