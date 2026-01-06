# Studio AI Multi-Agent

A library of specialized AI agents for development workflows, powered by OpenAI GPT-4o.

## Overview

This GitHub Action provides intelligent code analysis through specialized agents that automatically review your pull requests. Each agent focuses on a specific aspect of code quality:

- **Reviewer**: Critical code review focusing on readability, DRY principles, and architecture
- **Security**: Vulnerability scanning for injections, logic flaws, and sensitive data exposure
- **Documenter**: Technical writing to generate changelogs and release notes
- **Tester**: Automated unit test generation for new functions

## Usage

### Prerequisites

1. Add your OpenAI API key to your repository secrets:
   - Go to your repository Settings → Secrets and variables → Actions
   - Create a new secret named `OPENAI_API_KEY`
   - Paste your OpenAI API key

### Basic Configuration

In your GitHub workflow file (e.g., `.github/workflows/pr-review.yml`):

```yaml
name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Run AI Reviewer
        uses: nadescheemaeker/ai-core@main
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          agent_type: "reviewer"
```

### Agent Types

#### Code Reviewer

```yaml
- name: Code Review
  uses: nadescheemaeker/ai-core@main
  with:
    openai_api_key: ${{ secrets.OPENAI_API_KEY }}
    agent_type: "reviewer"
```

#### Security Scanner

```yaml
- name: Security Scan
  uses: nadescheemaeker/ai-core@main
  with:
    openai_api_key: ${{ secrets.OPENAI_API_KEY }}
    agent_type: "security"
```

#### Documentation Generator

```yaml
- name: Generate Documentation
  uses: nadescheemaeker/ai-core@main
  with:
    openai_api_key: ${{ secrets.OPENAI_API_KEY }}
    agent_type: "documenter"
```

#### Test Generator

```yaml
- name: Generate Tests
  uses: nadescheemaeker/ai-core@main
  with:
    openai_api_key: ${{ secrets.OPENAI_API_KEY }}
    agent_type: "tester"
```

### Multiple Agents

You can run multiple agents in the same workflow:

```yaml
name: Complete AI Analysis

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-analysis:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Code Review
        uses: nadescheemaeker/ai-core@main
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          agent_type: "reviewer"

      - name: Security Analysis
        uses: nadescheemaeker/ai-core@main
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          agent_type: "security"

      - name: Generate Tests
        uses: nadescheemaeker/ai-core@main
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          agent_type: "tester"

      - name: Generate Changelog
        uses: nadescheemaeker/ai-core@main
        with:
          openai_api_key: ${{ secrets.OPENAI_API_KEY }}
          agent_type: "documenter"
```

## Inputs

| Input            | Description                                                           | Required | Default    |
| ---------------- | --------------------------------------------------------------------- | -------- | ---------- |
| `openai_api_key` | OpenAI API Key                                                        | Yes      | -          |
| `agent_type`     | Agent type to launch (`reviewer`, `security`, `documenter`, `tester`) | No       | `reviewer` |

## How It Works

1. The action is triggered on pull request events
2. It retrieves the PR diff via GitHub API
3. The specified agent analyzes the changes using GPT-4o
4. Feedback is automatically posted as a comment on the PR

## Agent Details

### Reviewer Agent

- Analyzes code quality and architecture
- Suggests concrete improvements
- Focuses on readability and DRY principles
- Provides 3 actionable recommendations

### Security Agent

- Scans for security vulnerabilities
- Detects injection risks
- Identifies sensitive data exposure
- Provides fixes for found issues

### Documenter Agent

- Generates human-readable changelogs
- Creates release notes
- Summarizes technical impacts
- Helps with product documentation

### Tester Agent

- Identifies new functions in the diff
- Generates unit tests automatically
- Uses appropriate testing frameworks (Pytest, Jest, etc.)
- Provides ready-to-use test code

## Requirements

- OpenAI API key with access to GPT-4o
- GitHub repository with Actions enabled
- Pull request workflow

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
