import subprocess
from pathlib import Path

from ai_review.libs.logger import get_logger
from ai_review.services.git.types import GitServiceProtocol

logger = get_logger("GIT_SERVICE")


class GitService(GitServiceProtocol):
    def __init__(self, repo_dir: Path = Path(".")):
        self.repo_dir = repo_dir
        self._available_commits: set[str] = set()
        self._unavailable_commits: set[str] = set()

    def run_git(self, *args: str) -> str:
        cmd = ["git", *args]
        logger.debug(f"Running git command: {' '.join(cmd)} (cwd={self.repo_dir})")

        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_dir,
                capture_output=True,
                text=True,
                check=True,
            )
            if result.stderr.strip():
                logger.debug(f"Git stderr: {result.stderr.strip()}")
            return result.stdout
        except subprocess.CalledProcessError as error:
            logger.warning(
                f"Git command failed (exit={error.returncode}): {' '.join(cmd)}\n"
                f"stderr: {error.stderr.strip()}"
            )
            raise

    def get_diff(self, base_sha: str, head_sha: str, unified: int = 3) -> str:
        self._ensure_commits_available(base_sha, head_sha)
        return self.run_git("diff", f"--unified={unified}", base_sha, head_sha)

    def get_diff_for_file(self, base_sha: str, head_sha: str, file: str, unified: int = 3) -> str:
        if not file:
            logger.warning(f"Skipping git diff for empty filename (base={base_sha}, head={head_sha})")
            return ""

        self._ensure_commits_available(base_sha, head_sha)
        logger.debug(f"Generating diff for {file} between {base_sha}..{head_sha}")
        output = self.run_git("diff", f"--unified={unified}", base_sha, head_sha, "--", file)
        if not output.strip():
            logger.info(f"No diff found for {file} (possibly deleted or not tracked)")

        return output

    def get_changed_files(self, base_sha: str, head_sha: str) -> list[str]:
        self._ensure_commits_available(base_sha, head_sha)
        output = self.run_git("diff", "--name-only", base_sha, head_sha)
        files = [line.strip() for line in output.splitlines() if line.strip()]
        logger.debug(f"Changed files between {base_sha}..{head_sha}: {files}")
        return files

    def get_file_at_commit(self, file_path: str, sha: str) -> str | None:
        if not file_path:
            logger.warning(f"Skipping git show for empty file_path at {sha}")
            return None

        try:
            self._ensure_commits_available(sha)
            return self.run_git("show", f"{sha}:{file_path}")
        except subprocess.CalledProcessError as e:
            logger.warning(f"File '{file_path}' not found in commit {sha}: {e.stderr.strip()}")
            return None

    def _ensure_commits_available(self, *shas: str) -> None:
        missing = [sha for sha in shas if sha and not self._commit_available(sha)]
        if not missing:
            return

        missing_text = ", ".join(missing)
        message = (
            f"Git commits are not available locally: {missing_text}. "
            "This usually happens in CI with shallow clones. Configure the job with "
            "GIT_DEPTH=0, or fetch the merge request base/head commits before running ai-review."
        )
        logger.warning(message)
        raise RuntimeError(message)

    def _commit_available(self, sha: str) -> bool:
        if sha in self._available_commits:
            return True
        if sha in self._unavailable_commits:
            return False

        if self._commit_exists(sha):
            self._available_commits.add(sha)
            return True

        logger.info(f"Commit {sha} is missing locally; trying to fetch it from git remotes")
        self._fetch_missing_commit(sha)

        if self._commit_exists(sha):
            self._available_commits.add(sha)
            return True

        self._unavailable_commits.add(sha)
        return False

    def _commit_exists(self, sha: str) -> bool:
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
            cwd=self.repo_dir,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    def _fetch_missing_commit(self, sha: str) -> None:
        remotes = self._git_remotes()
        if not remotes:
            logger.warning("No git remotes configured; cannot fetch missing commit")
            return

        for remote in remotes:
            self._try_fetch(remote, sha)
            if self._commit_exists(sha):
                return

            if self._is_shallow_repository():
                self._try_unshallow(remote)
                if self._commit_exists(sha):
                    return

    def _git_remotes(self) -> list[str]:
        result = subprocess.run(
            ["git", "remote"],
            cwd=self.repo_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            logger.warning(f"Failed to list git remotes: {result.stderr.strip()}")
            return []
        return [remote.strip() for remote in result.stdout.splitlines() if remote.strip()]

    def _try_fetch(self, remote: str, sha: str) -> None:
        result = subprocess.run(
            ["git", "fetch", "--no-tags", "--depth=1000", remote, sha],
            cwd=self.repo_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            logger.debug(f"Failed to fetch commit {sha} from {remote}: {result.stderr.strip()}")

    def _try_unshallow(self, remote: str) -> None:
        result = subprocess.run(
            ["git", "fetch", "--no-tags", "--unshallow", remote],
            cwd=self.repo_dir,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            logger.debug(f"Failed to unshallow repository from {remote}: {result.stderr.strip()}")

    def _is_shallow_repository(self) -> bool:
        result = subprocess.run(
            ["git", "rev-parse", "--is-shallow-repository"],
            cwd=self.repo_dir,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0 and result.stdout.strip() == "true"
