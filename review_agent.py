import os
import requests
from openai import OpenAI

def main():
    # 1. Configuration
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    repo = os.getenv("GITHUB_REPOSITORY")
    pr_number = os.getenv("GITHUB_REF").split('/')[-2]
    
    # 2. Récupérer le diff de la PR via l'API GitHub
    headers = {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    diff_url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}"
    pr_data = requests.get(diff_url, headers=headers).json()
    diff_response = requests.get(pr_data['diff_url'], headers=headers)
    diff_text = diff_response.text

    # 3. Demander à l'IA
    prompt = f"En tant qu'expert tech du studio, analyse ce diff et donne 3 points d'amélioration majeurs :\n\n{diff_text}"
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    feedback = response.choices[0].message.content

    # 4. Poster le commentaire sur GitHub
    comment_url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    requests.post(comment_url, headers=headers, json={"body": f"### 🤖 Analyse de l'Agent Studio\n\n{feedback}"})

if __name__ == "__main__":
    main()
