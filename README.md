# AI Review

<p align="center">
  <img src="./docs/assets/logo.png" alt="Axiom logo" width="220" />
</p>

AI-powered code review tool.

[![License](https://img.shields.io/github/license/Nikita-Filonov/ai-review)](./LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Nikita-Filonov/ai-review?style=social)](https://github.com/Nikita-Filonov/ai-review/stargazers)
[![Support](https://img.shields.io/badge/Support-Boosty-orange)](https://boosty.to/ai_review)

_Made with ❤️ by [@NikitaFilonov](https://t.me/sound_right)_

---

## ❤️ Support AI Review

If AI Review helps you reduce noise in pull requests and saves time in code reviews, consider supporting its
development.

Your support helps to:

- improve review accuracy and reduce false positives
- expand integrations (GitHub, GitLab, Azure DevOps, etc.)
- develop new features and maintain the project

👉 https://boosty.to/ai_review

---

## 📑 Table of Contents

- ✨ [About](#-about)
- 🧪 [Live Preview](#-live-preview)
- 🚀 [Quick Start](#-quick-start)
- ⚙️ [️CI/CD Integration](#-cicd-integration)
    - 🚀 [GitLab CI/CD](#-gitlab-cicd)
- 📘 [Documentation](#-documentation)
- ⚠️ [Privacy & Responsibility Notice](#-privacy--responsibility-notice)

---

## ✨ About

**AI Review** is a developer tool that brings **AI-powered code review** directly into your workflow. It helps teams
improve code quality, enforce consistency, and speed up the review process.

✨ Key features:

- **Multiple LLM providers** — choose between **OpenAI**, **Claude**, **Gemini**, **Ollama**, **Bedrock**,
  **OpenRouter**, or **Azure OpenAI** and switch anytime.
- **VCS integration** — works out of the box with **GitLab**, **GitHub**, **Bitbucket Cloud**, **Bitbucket Server**,
  **Azure DevOps**, and **Gitea**.
- **Customizable prompts** — adapt inline, context, and summary reviews to match your team’s coding guidelines.
- **Agent mode** — iterative ReAct-style loop where the model can **explore the repository** with shell commands
  (`ls`, `cat`, `rg`, `git`) before producing a final review, giving it deeper context than a single-shot call.
- **Reply modes** — AI can now **participate in existing review threads**, adding follow-up replies in both inline and
  summary discussions.
- **Flexible configuration** — supports `YAML`, `JSON`, and `ENV`, with seamless overrides in CI/CD pipelines.
- **AI Review runs fully client-side** — it never proxies or inspects your requests.

AI Review runs automatically in your CI/CD pipeline and posts both **inline comments**, **summary reviews**, and now
**AI-generated replies** directly inside your merge requests. With **agent mode** enabled, the model can autonomously
explore the codebase before reviewing, resulting in more accurate and context-aware feedback. This makes reviews faster,
more conversational, and still fully under human control.

---

## 🧪 Live Preview

Curious how **AI Review** works in practice? Here are three real Pull Requests reviewed entirely by the tool — one per
mode:

| Mode             | Description                                                                                                                                  | 🐙 GitHub                                                             | 🦊 GitLab                                                                  | 🪣 Bitbucket                                                                        |
|------------------|----------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|----------------------------------------------------------------------------|-------------------------------------------------------------------------------------|
| 🧩 Inline        | Adds **line-by-line comments** directly in the diff. Focuses on specific code changes.                                                       | [View on GitHub](https://github.com/Nikita-Filonov/ai-review/pull/4)  | [View on GitLab](https://gitlab.com/core8332439/review/-/merge_requests/2) | [View on Bitbucket](https://bitbucket.org/test-5183/test-ai-review/pull-requests/2) |
| 🧠 Context       | Performs a **broader analysis across multiple files**, detecting cross-file issues and inconsistencies.                                      | [View on GitHub](https://github.com/Nikita-Filonov/ai-review/pull/5)  | [View on GitLab](https://gitlab.com/core8332439/review/-/merge_requests/3) | [View on Bitbucket](https://bitbucket.org/test-5183/test-ai-review/pull-requests/3) |
| 📄 Summary       | Posts a **concise high-level summary** with key highlights, strengths, and major issues.                                                     | [View on GitHub](https://github.com/Nikita-Filonov/ai-review/pull/6)  | [View on GitLab](https://gitlab.com/core8332439/review/-/merge_requests/4) | [View on Bitbucket](https://bitbucket.org/test-5183/test-ai-review/pull-requests/4) |
| 💬 Inline Reply  | Generates a **context-aware reply** to an existing inline comment thread. Can clarify decisions, propose fixes, or provide code suggestions. | [View on GitHub](https://github.com/Nikita-Filonov/ai-review/pull/16) | [View on GitLab](https://gitlab.com/core8332439/review/-/merge_requests/5) | [View on Bitbucket](https://bitbucket.org/test-5183/test-ai-review/pull-requests/5) |
| 💬 Summary Reply | Continues the **summary-level review discussion**, responding to reviewer comments with clarifications, rationale, or actionable next steps. | [View on GitHub](https://github.com/Nikita-Filonov/ai-review/pull/17) | [View on GitLab](https://gitlab.com/core8332439/review/-/merge_requests/6) | [View on Bitbucket](https://bitbucket.org/test-5183/test-ai-review/pull-requests/6) |

Available review modes:

```bash
ai-review run-inline
ai-review run-summary
ai-review run-context
ai-review run-inline-reply
ai-review run-summary-reply
```

---

## 🚀 Quick Start

Build the Docker image from this repository:

```bash
docker build -t ai-review:local .
```

Tag and push it to the registry used by your CI runners:

```bash
docker tag ai-review:local registry.example.com/ai-review:latest
docker push registry.example.com/ai-review:latest
```

Run AI Review against a checked-out repository:

```bash
docker run --rm \
  -v "$PWD:/workspace" \
  -w /workspace \
  --env-file .env \
  ai-review:local \
  ai-review run-summary
```

👉 Before running, create a basic configuration file [.ai-review.yaml](./docs/configs/.ai-review.yaml) in the root of
your project:

```yaml
llm:
  provider: OPENAI

  meta:
    model: gpt-4o-mini
    max_tokens: 1200
    temperature: 0.3

  http_client:
    timeout: 120
    api_url: https://api.openai.com/v1
    api_token: ${OPENAI_API_KEY}

vcs:
  provider: GITLAB

  pipeline:
    project_id: "1"
    merge_request_id: "100"

  http_client:
    timeout: 120
    api_url: https://gitlab.com
    api_token: ${GITLAB_API_TOKEN}
```

👉 This will:

- Run AI Review against your codebase.
- Generate inline and/or summary comments (depending on the selected mode).
- Use your chosen LLM provider (OpenAI GPT-4o-mini in this example).

> **Note:** Running `ai-review run` executes the full review (inline + summary).
> To run only one mode, use the dedicated subcommands:
> - ai-review run-inline
> - ai-review run-context
> - ai-review run-summary
> - ai-review run-inline-reply
> - ai-review run-summary-reply

---

AI Review can be configured via `.ai-review.yaml`, `.ai-review.json`, or `.env`. See [./docs/configs](./docs/configs)
for complete, ready-to-use examples.

Key things you can customize:

- **LLM provider** — OpenAI, Gemini, Claude, Ollama, Bedrock, OpenRouter, or Azure OpenAI
- **Model settings** — model name, temperature, max tokens
- **VCS integration** — works out of the box with **GitLab**, **GitHub**, **Bitbucket Cloud**, **Bitbucket Server**,
  **Azure DevOps**, and **Gitea**
- **Agent mode** — enable iterative repository exploration before review
- **Review policy** — which files to include/exclude, review modes
- **Prompts** — inline/context/summary/agent prompt templates

👉 Minimal configuration is enough to get started. Use the full reference configs if you want fine-grained control (
timeouts, artifacts, logging, etc.).

---

## ⚙️ CI/CD Integration

AI Review works out-of-the-box with major CI providers.
Use these snippets to run AI Review automatically on Pull/Merge Requests.  
Each integration uses environment variables for LLM and VCS configuration.

> For full configuration details (timeouts, artifacts, logging, prompt overrides), see [./docs/configs](./docs/configs).

### 🚀 GitLab CI/CD

For GitLab users:

```yaml
ai-review:
  when: manual
  stage: review
  image: registry.example.com/ai-review:latest
  rules:
    - if: '$CI_MERGE_REQUEST_IID'
  script:
    - ai-review run
  variables:
    GIT_DEPTH: "0"

    # --- LLM configuration ---
    LLM__PROVIDER: "OPENAI"
    LLM__META__MODEL: "gpt-4o-mini"
    LLM__META__MAX_TOKENS: "15000"
    LLM__META__TEMPERATURE: "0.3"
    LLM__HTTP_CLIENT__API_URL: "https://api.openai.com/v1"
    LLM__HTTP_CLIENT__API_TOKEN: "$OPENAI_API_KEY"

    # --- GitLab integration ---
    VCS__PROVIDER: "GITLAB"
    VCS__PIPELINE__PROJECT_ID: "$CI_PROJECT_ID"
    VCS__PIPELINE__MERGE_REQUEST_ID: "$CI_MERGE_REQUEST_IID"
    VCS__HTTP_CLIENT__API_URL: "$CI_SERVER_URL"
    VCS__HTTP_CLIENT__API_TOKEN: "$CI_JOB_TOKEN"
  allow_failure: true  # Optional: don't block pipeline if AI review fails

```

🔗 Full example: [./docs/ci/gitlab.yaml](./docs/ci/gitlab.yaml)

---

## 📘 Documentation

See these folders for reference templates and full configuration options:

- [./docs/ci](./docs/ci) — CI/CD integration templates for Docker-based CI jobs
- [./docs/cli](./docs/cli) — CLI command reference and usage examples
- [./docs/hooks](./docs/hooks) — hook reference and lifecycle events
- [./docs/configs](./docs/configs) — full configuration examples (`.yaml`, `.json`, `.env`)
- [./docs/prompts](./docs/prompts) — prompt templates for Python/Go (light & strict modes)
- [./docs/troubleshooting.md](./docs/troubleshooting) — common environment and Git-related issues

---

## ⚠️ Privacy & Responsibility Notice

AI Review does **not store**, **log**, or **transmit** your source code to any external service other than the **LLM
provider** explicitly configured in your `.ai-review.yaml`.

All data is sent **directly** from your CI/CD environment to the selected LLM API endpoint (e.g. OpenAI, Gemini,
Claude, OpenRouter). No intermediary servers or storage layers are involved.

If you use **Ollama**, requests are sent to your **local or self-hosted Ollama runtime**  
(by default `http://localhost:11434`). This allows you to run reviews completely **offline**, keeping all data strictly
inside your infrastructure.

> ⚠️ Please ensure you use proper API tokens and avoid exposing corporate or personal secrets.
> If you accidentally leak private code or credentials due to incorrect configuration (e.g., using a personal key
> instead of an enterprise one), it is **your responsibility** — the tool does not retain or share any data by itself.

---

🧠 **AI Review** — open-source AI-powered code reviewer

Build it locally with Docker and run it inside your own CI infrastructure.
