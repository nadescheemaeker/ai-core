# Studio AI Multi-Agent

A library of specialized AI agents for development workflows, powered by LiteLLM for multi-model support.

## Overview

This GitHub Action provides intelligent code analysis through specialized agents that automatically review your pull requests. Thanks to LiteLLM integration, you can use any AI provider (OpenAI, Anthropic Claude, Google Gemini, and more). Each agent focuses on a specific aspect of code quality:

- **Reviewer**: Critical code review focusing on readability, DRY principles, and architecture
- **Security**: Vulnerability scanning for injections, logic flaws, and sensitive data exposure
- **Documenter**: Technical writing to generate changelogs and release notes
- **Tester**: Automated unit test generation for new functions

### Smart Standards System

The action automatically loads relevant coding standards based on the files changed in your PR:

- **Global standards** (`standards/global.md`): Applied to all projects
- **Language-specific standards**: Automatically loaded based on file extensions
  - `standards/csharp.md` for `.cs` files
  - `standards/react.md` for `.jsx`, `.tsx` files
  - `standards/python.md` for `.py` files
  - And more...

This ensures that AI agents provide feedback aligned with your team's coding conventions and best practices.

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
3. **Smart standards loading**: Automatically detects file types in the diff and loads relevant coding standards
4. The specified agent analyzes the changes using your chosen AI model (via LiteLLM) with the loaded standards as context
5. Feedback is automatically posted as a comment on the PR, aligned with your coding standards

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

## Project Structure

```
ai-core/
├── action.yml              # GitHub Action configuration
├── main_launcher.py        # Main entry point with smart standards loading
├── agents/                 # Specialized AI agents
│   ├── reviewer_agent.py
│   ├── security_agent.py
│   ├── documenter_agent.py
│   └── tester_agent.py
└── standards/              # Coding standards (optional)
    ├── global.md           # Universal standards for all projects
    ├── csharp.md           # C# specific standards
    ├── react.md            # React/TypeScript standards
    └── python.md           # Python standards (add your own)
```

### Customizing Standards

You can customize the coding standards by:

1. **Fork this repository** or use it as a template
2. **Edit the standards files** in the `standards/` directory to match your team's conventions
3. **Add new standards files** for other languages (e.g., `java.md`, `go.md`)
4. **Update the mapping** in `main_launcher.py` to associate file extensions with your new standards files

The system will automatically load the relevant standards based on the file extensions detected in your PR diffs.

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
