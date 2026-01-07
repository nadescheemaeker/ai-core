import os
import sys
import requests
import importlib
from litellm import completion

# --- PATH CONFIGURATION ---
# Get the absolute path of the directory where this script is located (ai-core)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Add BASE_DIR to path so that 'import agents.xxx' works
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

def get_relevant_standards(diff_text):
    """Load Markdown standards using absolute paths."""
    standards_content = ""
    # Absolute path to the standards folder
    standards_path = os.path.join(BASE_DIR, "standards")
    
    if not os.path.exists(standards_path):
        print(f"DEBUG: Standards folder not found at {standards_path}")
        return ""

    # 1. Global Standard
    global_path = os.path.join(standards_path, "global.md")
    if os.path.exists(global_path):
        with open(global_path, 'r', encoding='utf-8') as f:
            standards_content += f"\n--- GLOBAL STANDARDS ---\n{f.read()}\n"

    # 2. Detect extensions in the diff
    detected_exts = set()
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            ext = line.split('.')[-1].lower()
            detected_exts.add(ext)

    # 3. Specific standards
    mapping = {"py": "python.md", "js": "javascript.md", "jsx": "react.md", "tsx": "react.md", "cs": "csharp.md"}
    for ext in detected_exts:
        std_file = mapping.get(ext)
        if std_file:
            path = os.path.join(standards_path, std_file)
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    standards_content += f"\n--- {ext.upper()} STANDARDS ---\n{f.read()}\n"

    return standards_content

def main():
    # Get environment variables
    api_key = os.getenv("CUSTOM_API_KEY")
    agent_type = os.getenv("AGENT_TYPE", "reviewer")
    model_name = os.getenv("MODEL_NAME", "gpt-4o")
    github_token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("GITHUB_REF").split('/')[-2]

    # 1. Retrieve the Diff
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3.diff"}
    diff_text = requests.get(f"https://api.github.com/repos/{repo}/pulls/{pr_number}", headers=headers).text

    # 2. Dynamic Agent Loading
    try:
        # Thanks to sys.path.append(BASE_DIR), this will now work
        agent_module = importlib.import_module(f"agents.{agent_type}_agent")
        prompts = agent_module.get_prompt(diff_text)
    except ImportError as e:
        print(f"Error importing agent '{agent_type}': {e}")
        sys.exit(1)

    # 3. Load Relevant Standards
    relevant_standards = get_relevant_standards(diff_text)
    system_message = f"{prompts['system']}\n\nHERE ARE THE STANDARDS TO FOLLOW:\n{relevant_standards}"

    # 4. AI Call and Publish Feedback (LiteLLM) with Error Handling
    try:
        response = completion(
            model=model_name,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompts["user"]}
            ],
            api_key=api_key
        )
        
        feedback = response.choices[0].message.content
        
    except litellm.RateLimitError as e:
        # Check specifically for billing quota issues
        if "insufficient_quota" in str(e):
            print("CRITICAL: OpenAI Billing Hard Limit Reached.")
            feedback = "⚠️ **AI Review Failed:** The OpenAI API quota has been exceeded. Please check billing details."
        else:
            print(f"Rate limit hit: {e}")
            feedback = "⚠️ **AI Review Failed:** Rate limit exceeded. Please re-run the job later."
            
    except Exception as e:
        print(f"Unexpected error: {e}")
        feedback = f"⚠️ **AI Review Failed:** An unexpected error occurred: {e}"

    # 5. Post the result (either the review or the error message)
    comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    requests.post(comment_url, headers={"Authorization": f"token {github_token}"}, json={"body": feedback})
    
if __name__ == "__main__":
    main()
