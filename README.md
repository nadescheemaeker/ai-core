# Studio AI Multi-Agent

A library of specialized AI agents for development workflows, powered by LiteLLM for multi-model support.

## Overview

This GitHub Action provides intelligent code analysis through specialized agents that automatically review your pull requests. Thanks to LiteLLM integration, you can use any AI provider (OpenAI, Anthropic Claude, Google Gemini, and more). Each agent focuses on a specific aspect of code quality:

- **Reviewer**: Critical code review focusing on readability, DRY principles, and architecture
- **Security**: Vulnerability scanning for injections, logic flaws, and sensitive data exposure
- **Documenter**: Technical writing to generate changelogs and release notes
- **Tester**: Automated unit test generation for new functions

## Usage

### Prerequisites

1. Add your AI provider API key to your repository secrets:
   - Go to your repository Settings → Secrets and variables → Actions
   - Create a new secret named `AI_API_KEY` (or `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.)
   - Paste your API key from your chosen provider

### Supported Models

Thanks to LiteLLM, you can use any of these AI providers:

- **OpenAI**: `gpt-4o`, `gpt-4-turbo`, `gpt-3.5-turbo`
- **Anthropic**: `claude-3-5-sonnet-20240620`, `claude-3-opus-20240229`
- **Google**: `gemini/gemini-1.5-pro`, `gemini/gemini-1.5-flash`
- **And many more**: See [LiteLLM documentation](https://docs.litellm.ai/docs/providers) for the full list

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
          api_key: ${{ secrets.AI_API_KEY }}
          agent_type: "reviewer"
          model_name: "gpt-4o" # Optional, defaults to gpt-4o
```

### Using Different AI Models

#### OpenAI GPT-4o (default)

```yaml
- name: Code Review with GPT-4o
  uses: nadescheemaeker/ai-core@main
  with:
    api_key: ${{ secrets.OPENAI_API_KEY }}
    agent_type: "reviewer"
    model_name: "gpt-4o"
```

#### Anthropic Claude

```yaml
- name: Code Review with Claude
  uses: nadescheemaeker/ai-core@main
  with:
    api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    agent_type: "reviewer"
    model_name: "claude-3-5-sonnet-20240620"
```

#### Google Gemini

```yaml
- name: Code Review with Gemini
  uses: nadescheemaeker/ai-core@main
  with:
    api_key: ${{ secrets.GOOGLE_API_KEY }}
    agent_type: "reviewer"
    model_name: "gemini/gemini-1.5-pro"
```

### Agent Types

#### Code Reviewer

```yaml
- name: Code Review
  uses: nadescheemaeker/ai-core@main
  with:
    api_key: ${{ secrets.AI_API_KEY }}
    agent_type: "reviewer"
```

#### Security Scanner

```yaml
- name: Security Scan
  uses: nadescheemaeker/ai-core@main
  with:
    api_key: ${{ secrets.AI_API_KEY }}
    agent_type: "security"
```

#### Documentation Generator

```yaml
- name: Generate Documentation
  uses: nadescheemaeker/ai-core@main
  with:
    api_key: ${{ secrets.AI_API_KEY }}
    agent_type: "documenter"
```

#### Test Generator

```yaml
- name: Generate Tests
  uses: nadescheemaeker/ai-core@main
  with:
    api_key: ${{ secrets.AI_API_KEY }}
    agent_type: "tester"
```

### Multiple Agents

You can run multiple agents in the same workflow, even with different models:

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

      - name: Code Review with GPT-4o
        uses: nadescheemaeker/ai-core@main
        with:
          api_key: ${{ secrets.OPENAI_API_KEY }}
          agent_type: "reviewer"
          model_name: "gpt-4o"

      - name: Security Analysis with Claude
        uses: nadescheemaeker/ai-core@main
        with:
          api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          agent_type: "security"
          model_name: "claude-3-5-sonnet-20240620"

      - name: Generate Tests with Gemini
        uses: nadescheemaeker/ai-core@main
        with:
          api_key: ${{ secrets.GOOGLE_API_KEY }}
          agent_type: "tester"
          model_name: "gemini/gemini-1.5-pro"

      - name: Generate Changelog with GPT-4
        uses: nadescheemaeker/ai-core@main
        with:
          api_key: ${{ secrets.OPENAI_API_KEY }}
          agent_type: "documenter"
          model_name: "gpt-4-turbo"
```

## Inputs

| Input        | Description                                                           | Required | Default    |
| ------------ | --------------------------------------------------------------------- | -------- | ---------- |
| `api_key`    | API Key for your chosen AI provider                                   | Yes      | -          |
| `agent_type` | Agent type to launch (`reviewer`, `security`, `documenter`, `tester`) | No       | `reviewer` |
| `model_name` | AI model to use (e.g., `gpt-4o`, `claude-3-5-sonnet-20240620`)        | No       | `gpt-4o`   |

## How It Works

1. The action is triggered on pull request events
2. It retrieves the PR diff via GitHub API
3. The specified agent analyzes the changes using your chosen AI model (via LiteLLM)
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

- API key for your chosen AI provider (OpenAI, Anthropic, Google, etc.)
- GitHub repository with Actions enabled
- Pull request workflow

## Why LiteLLM?

LiteLLM provides:

- **Multi-provider support**: Switch between OpenAI, Anthropic, Google, and 100+ models
- **Unified API**: Same code works with all providers
- **Cost optimization**: Choose the most cost-effective model for each task
- **Flexibility**: Test different models to find the best fit for your needs

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
