# 📘 AI Review Troubleshooting

This document describes common environment-related issues when running **ai-review**. All cases below are expected Git /
CI behavior, not bugs in `ai-review`.

---

## 🧩 Non-ASCII (Cyrillic) filenames break diff parsing

### Symptoms

- Diff is empty or files are not matched
- Inline review does not work for files with Cyrillic names

### Cause

By default, Git escapes non-ASCII paths in diff output (`core.quotepath=true`).

### Solution

`ai-review` [Docker image](./../../Dockerfile) sets this automatically:

```bash
git config --global core.quotepath false
````

If running outside Docker, make sure this option is enabled manually.

---

## 🧩 `git diff` fails with exit code 128 (missing commits)

### Symptoms

```text
git diff <BASE_SHA> <HEAD_SHA> ... returned exit status 128
fatal: bad object <BASE_SHA>
```

### Cause

One of the compared commits is not present locally. This usually happens due to **shallow clones in CI**.

For GitLab merge requests this can also appear when the GitLab API returns a changed file with:

```json
{
  "collapsed": true,
  "diff": ""
}
```

In that case `ai-review` must reconstruct the patch through local `git diff`, so the checkout must contain both
`diff_refs.base_sha` and `diff_refs.head_sha`.

### Solution

Fetch full Git history before running `ai-review`.

#### GitLab CI

```yaml
variables:
  GIT_DEPTH: 0
```

Or manually:

```bash
git fetch --unshallow
```

To verify the job has the required commits, run this in the same CI job before `ai-review run`:

```bash
git cat-file -e "$BASE_SHA^{commit}"
git cat-file -e "$HEAD_SHA^{commit}"
```

For GitLab CI you can use the MR diff refs from the API response, or print the exact SHAs from the `ai-review` logs.

