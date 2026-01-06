import os
import requests
import importlib
import sys
from litellm import completion

def get_relevant_standards(diff_text):
    """Analyze the diff to load only the relevant .md files."""
    standards_content = ""
    standards_path = os.path.join(os.path.dirname(__file__), "standards")
    
    if not os.path.exists(standards_path):
        return ""

    # 1. Always load the global standard if it exists
    global_path = os.path.join(standards_path, "global.md")
    if os.path.exists(global_path):
        with open(global_path, 'r') as f:
            standards_content += f"\n--- GLOBAL STANDARDS ---\n{f.read()}\n"

    # 2. Detect extensions in the diff (e.g., .py, .js, .tsx)
    # We look for lines like '+++ b/path/to/file.js'
    detected_exts = set()
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            ext = line.split('.')[-1].lower()
            detected_exts.add(ext)

    # 3. Load corresponding standards (e.g., if .js detected, look for js.md)
    mapping = {
        "py": "python.md",
        "js": "javascript.md",
        "jsx": "react.md",
        "tsx": "react.md",
        "ts": "typescript.md",
        "css": "style.md"
    }

    for ext in detected_exts:
        std_file = mapping.get(ext)
        if std_file:
            path = os.path.join(standards_path, std_file)
            if os.path.exists(path):
                with open(path, 'r') as f:
                    standards_content += f"\n--- SPECIFIC STANDARDS ({ext.upper()}) ---\n{f.read()}\n"

    return standards_content

def main():
    api_key = os.getenv("CUSTOM_API_KEY")
    agent_type = os.getenv("AGENT_TYPE", "reviewer")
    model_name = os.getenv("MODEL_NAME", "gpt-4o")
    github_token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    
    # Retrieve the Diff
    pr_number = os.getenv("GITHUB_REF").split('/')[-2]
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3.diff"}
    diff_text = requests.get(f"https://api.github.com/repos/{repo}/pulls/{pr_number}", headers=headers).text

    # Load relevant standards
    relevant_standards = get_relevant_standards(diff_text)

    # Load the agent
    agent_module = importlib.import_module(f"agents.{agent_type}")
    prompts = agent_module.get_prompt(diff_text)

    # Inject standards into the system message
    system_message = f"{prompts['system']}\n\nSTUDIO GUIDELINES AND STANDARDS:\n{relevant_standards}"

    # AI Call
    response = completion(
        model=model_name,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompts["user"]}
        ],
        api_key=api_key
    )
    
    # Publish feedback
    feedback = response.choices[0].message.content
    comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    requests.post(comment_url, headers={"Authorization": f"token {github_token}"}, json={"body": feedback})

if __name__ == "__main__":
    main()