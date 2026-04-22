# 📘 AI Review CI/CD Integration

This folder contains **ready-to-use CI/CD templates** for running AI Review from a Docker image on Pull/Merge Requests.

Each example shows how to:

- Use a prebuilt AI Review Docker image
- Pass LLM and VCS credentials securely via environment variables
- Trigger inline, summary, or context review commands

Build and publish the image before using these templates:

```bash
docker build -t ai-review:local .
docker tag ai-review:local registry.example.com/ai-review:latest
docker push registry.example.com/ai-review:latest
```

---

## ⚙️ Supported CI/CD Providers

| Provider     | Template                                 | Description                                                                    |
|--------------|------------------------------------------|--------------------------------------------------------------------------------|
| GitLab       | [gitlab.yaml](./gitlab.yaml)             | Manual job trigger in Merge Request pipelines                                  |
| Jenkins      | [Jenkinsfile](./Jenkinsfile)             | Declarative pipeline with **inline/context/summary** review stages             |
| Bitbucket    | [bitbucket.yaml](./bitbucket.yaml)       | Manual custom pipeline trigger per Pull Request (supports all AI Review modes) |
| Azure DevOps | [azure-devops.yaml](./azure-devops.yaml) | Manual or PR-triggered pipeline in **Azure Pipelines**                         |

---

👉 Choose the template matching your CI system, copy it into your repository, and adjust environment
variables (`OPENAI_API_KEY`, `GITHUB_TOKEN`, `CI_JOB_TOKEN`, `BITBUCKET_TOKEN`, etc.) as needed.
