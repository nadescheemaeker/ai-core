import os
import requests
import importlib
import sys
from litellm import completion # <--- Universal import

def main():
    api_key = os.getenv("CUSTOM_API_KEY")
    agent_type = os.getenv("AGENT_TYPE", "reviewer")
    model_name = os.getenv("MODEL_NAME", "gpt-4o")
    github_token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    
    try:
        pr_number = os.getenv("GITHUB_REF").split('/')[-2]
    except:
        sys.exit(1)

    # 1. Retrieve Diff
    headers = {"Authorization": f"token {github_token}", "Accept": "application/vnd.github.v3.diff"}
    diff_text = requests.get(f"https://api.github.com/repos/{repo}/pulls/{pr_number}", headers=headers).text

    # 2. Load agent
    agent_module = importlib.import_module(f"agents.{agent_type}")
    prompts = agent_module.get_prompt(diff_text)

    # 3. Multi-Model Call
    # LiteLLM handles the format based on the model prefix
    try:
        response = completion(
            model=model_name,
            messages=[
                {"role": "system", "content": prompts["system"]},
                {"role": "user", "content": prompts["user"]}
            ],
            api_key=api_key
        )
        feedback = response.choices[0].message.content
    except Exception as e:
        print(f"Error with model {model_name}: {e}")
        sys.exit(1)

    # 4. Publish to GitHub
    comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    payload = {"body": f"## 🤖 Agent {agent_type.upper()} ({model_name})\n\n{feedback}"}
    requests.post(comment_url, headers={"Authorization": f"token {github_token}"}, json=payload)

if __name__ == "__main__":
    main()