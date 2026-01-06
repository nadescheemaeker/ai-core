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

### When to Use What?

This project uses **LiteLLM** by default, which is perfect for:

- ✅ **Rapid prototyping**: Get started quickly with minimal setup
- ✅ **Multi-provider support**: Easy switching between AI providers
- ✅ **Small to medium workloads**: GitHub Actions, personal projects, team tools
- ✅ **Simplicity**: Straightforward integration without complex infrastructure

### Production Alternatives for High-Scale Workloads

For production environments with high traffic and demanding requirements, consider these enterprise-grade alternatives:

#### TrueFoundry

[TrueFoundry](https://www.truefoundry.com/) is designed for production ML deployments:

- **Infrastructure management**: Auto-scaling, monitoring, and cost optimization
- **Model serving**: High-throughput inference with load balancing
- **Observability**: Built-in logging, metrics, and tracing
- **Multi-cloud support**: Deploy on AWS, GCP, Azure, or on-premises

**Best for**: Teams needing enterprise-grade ML infrastructure with DevOps automation.

#### Portkey

[Portkey](https://portkey.ai/) is an AI gateway focused on reliability and control:

- **Load balancing**: Distribute requests across multiple providers/models
- **Fallback & retries**: Automatic failover when a provider is down
- **Caching**: Reduce costs and latency with intelligent caching
- **Rate limiting & quotas**: Fine-grained control over API usage
- **Analytics & monitoring**: Detailed insights into usage, costs, and performance
- **Prompt management**: Version control and A/B testing for prompts

**Best for**: Production applications requiring high reliability, cost control, and observability.

#### Migration Path

The architecture is designed to be modular. To migrate from LiteLLM to TrueFoundry or Portkey:

1. Replace the `completion()` call in `main_launcher.py` with your chosen provider's SDK
2. Update environment variables for authentication
3. Adjust configuration for caching, retries, and load balancing as needed

The rest of the agent logic remains unchanged.

## Future Roadmap

### Self-Healing PRs (Auto-Correction)

Currently, agents post comments with suggestions. The next evolution is **automatic code correction**:

**The Vision**: When the security agent detects a vulnerability, it doesn't just explain it—it generates and proposes the actual fix.

**Implementation Approaches**:

- Use GitHub's **suggested changes** feature in pull request review comments
- Create a new commit on the PR branch with the corrected code
- Open a separate "fix PR" that targets the original PR branch
- Use GitHub's `check_run` API to provide inline code suggestions

**Example Flow**:

1. Security agent detects an SQL injection vulnerability
2. Generates sanitized code with parameterized queries
3. Posts the fix as a GitHub suggestion that the developer can accept with one click

### Long-Term Memory (Studio Knowledge Base)

Current agents only see the current PR. The next step is **contextual awareness across your entire codebase and project history**.

**RAG (Retrieval-Augmented Generation) Integration**:

- Index all repositories, documentation, and tickets (Jira/Linear) in a vector database (Pinecone, Milvus, Weaviate)
- Enable agents to search historical context before providing feedback

**Enhanced Capabilities**:

- **Historical Pattern Recognition**: "Warning: You're modifying this function. We had a similar bug in Project X 6 months ago related to cache management."
- **Cross-Repository Learning**: "This authentication pattern was deprecated in favor of OAuth2 in the API service repository."
- **Ticket Correlation**: "This change addresses JIRA-1234, but doesn't implement the caching requirement mentioned in the spec."

**Technical Implementation**:

```python
# Pseudocode example
def get_relevant_context(diff_text):
    # Embed the current changes
    embeddings = embed_code(diff_text)

    # Search vector database for similar patterns
    similar_issues = vector_db.search(embeddings, limit=5)
    similar_code = vector_db.search_code(embeddings, limit=3)

    # Augment agent prompt with historical context
    return f"Related past issues: {similar_issues}\nSimilar code patterns: {similar_code}"
```

### Project Management & Onboarding Agents

Extend AI capabilities beyond pure code review to **team productivity and knowledge management**.

#### Spec Validator Agent

**Purpose**: Ensure PRs actually implement what was specified in the ticket.

**How It Works**:

- Fetches the original Jira/Linear ticket linked to the PR
- Extracts acceptance criteria and requirements
- Compares PR changes against the specification
- Flags missing features or scope creep

**Example Output**:

```
⚠️ Spec Validation Issues:
- ✅ User authentication implemented
- ✅ Password validation added
- ❌ Missing: "Remember me" functionality (JIRA-1234, AC-3)
- ⚠️ Out of scope: Dark mode toggle (not in original ticket)
```

#### Onboarding Assistant Agent

**Purpose**: Help new developers understand your codebase through natural language queries.

**Capabilities**:

- Answer questions like "How does our deployment pipeline work?"
- Provide code examples: "Show me how to add a new API endpoint"
- Explain architecture: "What's the difference between UserService and AuthService?"
- Generate onboarding documentation automatically

**Implementation**:

- Index codebase, README files, and documentation
- Create a chatbot interface (Slack bot, GitHub Discussions, or web UI)
- Use RAG to provide accurate, repository-specific answers

### 📊 Studio Analytics Dashboard

Track and optimize your AI agents' performance with comprehensive metrics.

#### Key Metrics to Track

**1. Acceptance Rate**

- How many AI suggestions are actually accepted by developers?
- Which agent types provide the most valuable feedback?
- Track by team, repository, and time period

**2. Cost Management**

- Token consumption per PR
- Cost breakdown by agent type and model
- Budget alerts and optimization recommendations

**3. Code Quality Impact**

- Bugs in production before vs. after AI-core adoption
- Time to fix issues (with AI suggestions vs. without)
- Code review cycle time reduction

**4. Agent Performance**

- Response time per agent
- Model effectiveness (GPT-4 vs. Claude vs. Gemini)
- False positive rate for security/quality issues

#### Sample Dashboard Metrics

```
Studio AI Analytics - December 2025
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Performance
  • PRs Analyzed: 1,247
  • Suggestions Made: 3,891
  • Acceptance Rate: 68%
  • Avg. Review Time: 12 min (↓45% from baseline)

Cost Breakdown
  • Total Spend: $287.50
  • Cost per PR: $0.23
  • Most Used Model: GPT-4o (72%)

Quality Impact
  • Production Bugs: 12 (↓38% vs. last quarter)
  • Security Issues Prevented: 47
  • Code Coverage: 87% (↑12%)

Agent Statistics
  • Reviewer: 542 PRs (71% acceptance)
  • Security: 198 PRs (89% acceptance)
  • Tester: 312 PRs (54% acceptance)
  • Documenter: 195 PRs (82% acceptance)
```

#### Implementation Options

**Data Collection**:

- Store agent interactions in a database (PostgreSQL, MongoDB)
- Track GitHub API events and PR metadata
- Log token usage and model choices

**Visualization**:

- Build a custom dashboard with React/Next.js + Chart.js
- Use existing tools like Grafana, Metabase, or Retool
- GitHub Actions summary reports

**Actionable Insights**:

- Automatically adjust model selection based on cost/performance
- Identify which standards need clarification (high rejection rate)
- A/B test different prompts and agents

### Getting Started with Advanced Features

These features represent the evolution of AI-core from a simple code review tool to a **comprehensive AI development studio**. We welcome contributions in any of these areas!

**Priority Roadmap**:

1. **Phase 1**: Self-healing PRs with GitHub suggestions
2. **Phase 2**: Basic analytics dashboard
3. **Phase 3**: RAG integration for long-term memory
4. **Phase 4**: Project management agents

See our [Contributing Guide](#contributing) to get involved.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
