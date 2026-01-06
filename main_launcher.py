import os
import requests
import importlib
import sys
from openai import OpenAI

def main():
    # 1. Retrieve environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    agent_type = os.getenv("AGENT_TYPE", "reviewer") # Default 'reviewer'
    github_token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPOSITORY")
    
    # Extract PR number from GITHUB_REF (e.g., refs/pull/42/merge)
    try:
        pr_number = os.getenv("GITHUB_REF").split('/')[-2]
    except Exception:
        print("Error: Unable to determine Pull Request number.")
        sys.exit(1)

    if not api_key:
        print("Error: OPENAI_API_KEY missing.")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    # 2. Retrieve PR Diff via GitHub API
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3.diff"
    }
    
    diff_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    response_diff = requests.get(diff_url, headers=headers)
    
    if response_diff.status_code != 200:
        print(f"GitHub API Error: {response_diff.status_code}")
        sys.exit(1)
        
    diff_text = response_diff.text

    # 3. Load specific agent
    try:
        # Dynamic import from 'agents' folder
        # Make sure you have an empty __init__.py file in the agents/ folder
        module_path = f"agents.{agent_type}"
        agent_module = importlib.import_module(module_path)
        prompts = agent_module.get_prompt(diff_text)
    except ImportError:
        print(f"Error: Agent '{agent_type}' not found in agents/ folder.")
        sys.exit(1)

    # 4. AI Call (GPT-4o)
    print(f"Launching agent: {agent_type}...")
    try:
        ai_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompts["system"]},
                {"role": "user", "content": prompts["user"]}
            ],
            temperature=0.2 # Low temperature for more technical precision
        )
        feedback = ai_response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI Error: {e}")
        sys.exit(1)

    # 5. Post comment on PR
    comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    payload = {
        "body": f"## 🤖 Studio AI: Agent {agent_type.capitalize()}\n\n{feedback}"
    }
    # Reset headers for JSON
    headers["Accept"] = "application/vnd.github.v3+json"
    requests.post(comment_url, headers=headers, json=payload)
    print(f"Agent {agent_type} comment posted successfully.")

if __name__ == "__main__":
    main()