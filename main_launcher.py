import os
import sys
import requests
import importlib
import litellm
from litellm import completion

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

def get_relevant_standards(diff_text):
    """Load Markdown standards using absolute paths."""
    standards_content = ""
    standards_path = os.path.join(BASE_DIR, "standards")
    
    if not os.path.exists(standards_path):
        return ""

    global_path = os.path.join(standards_path, "global.md")
    if os.path.exists(global_path):
        with open(global_path, 'r', encoding='utf-8') as f:
            standards_content += f"\n--- GLOBAL STANDARDS ---\n{f.read()}\n"

    detected_exts = set()
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            ext = line.split('.')[-1].lower()
            detected_exts.add(ext)

    mapping = {"py": "python.md", "js": "javascript.md", "jsx": "react.md", "tsx": "react.md", "cs": "csharp.md"}
    for ext in detected_exts:
        std_file = mapping.get(ext)
        if std_file and os.path.exists(os.path.join(standards_path, std_file)):
            with open(os.path.join(standards_path, std_file), 'r', encoding='utf-8') as f:
                standards_content += f"\n--- {ext.upper()} STANDARDS ---\n{f.read()}\n"

    return standards_content

def main():
    # 1. Configuration
    api_key = os.getenv("CUSTOM_API_KEY")
    model_name = os.getenv("MODEL_NAME", "azure/gpt-4o") # Prefix with azure/
    
    # Azure Specific Variables
    os.environ["AZURE_API_KEY"] = api_key
    os.environ["AZURE_API_BASE"] = os.getenv("AZURE_API_BASE")       # e.g. https://your-resource.openai.azure.com/
    os.environ["AZURE_API_VERSION"] = os.getenv("AZURE_API_VERSION") # e.g. 2024-05-01-preview
    
    agent_type = os.getenv("AGENT_TYPE", "reviewer")
    github_token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("GITHUB_REF").split('/')[-2]

    # 2. Retrieve the Diff
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3.diff"}
    diff_text = requests.get(f"https://api.github.com/repos/{repo}/pulls/{pr_number}", headers=headers).text

    # 3. Dynamic Agent Loading
    try:
        module_name = f"agents.{agent_type}_agent"
        agent_module = importlib.import_module(module_name)
        prompts = agent_module.get_prompt(diff_text)
    except ImportError as e:
        print(f"Error importing agent '{agent_type}': {e}")
        sys.exit(1)

    # 4. Standards
    relevant_standards = get_relevant_standards(diff_text)
    system_message = f"{prompts['system']}\n\nHERE ARE THE STANDARDS TO FOLLOW:\n{relevant_standards}"

    # 5. AI Call (Azure Support via LiteLLM)
    try:
        # LiteLLM routes to Azure if model starts with "azure/"
        response = completion(
            model=model_name,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompts["user"]}
            ]
        )
        feedback = response.choices[0].message.content
        
    except Exception as e:
        print(f"Error: {e}")
        feedback = f"⚠️ **AI Review Failed:** {str(e)}"

    # 6. Post result
    comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    requests.post(comment_url, headers={"Authorization": f"token {github_token}"}, json={"body": feedback})
    
if __name__ == "__main__":
    main()
