import os
import subprocess


class GitHandler:
    def __init__(self):
        self.repo_path = os.getcwd()

    def is_repo_clean(self):
        """
        Check if the Git repository has any changes.
        """
        status = self.run_git_command(["git", "status", "--porcelain"])
        return len(status) == 0

    def run_git_command(self, command):
        """
        Run a git command and return its output.
        """
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout

    def get_git_diff(self, branch1, branch2):
        """
        Get git diff between two branches
        :param branch1: First branch
        :param branch2: Second branch
        :return: Git diff
        """
        command = ["git", "diff", branch1, branch2]
        return self.run_git_command(command)

    def parse_git_diff(self, diff):
        """
        Parse git diff and return a list of modified files
        :param diff: Git diff
        :return: List of modified files
        """
        modified_files = []
        for line in diff.split('\n'):
            if line.startswith('+++ b/'):
                modified_files.append(line[6:])
        return modified_files

    def get_git_branch(self):
        """
        Get current git branch
        :return: Current git branch
        """
        command = ["git", "rev-parse", "--abbrev-ref", "HEAD"]
        return self.run_git_command(command).strip()

    def get_git_remote(self):
        """
        Get current git remote
        :return: Current git remote
        """
        command = ["git", "config", "--get", "remote.origin.url"]
        return self.run_git_command(command).strip()

    def get_git_repo_name(self):
        """
        Get current git repo name
        :return: Current git repo name
        """
        command = ["basename", "-s", ".git", self.get_git_remote()]
        return self.run_git_command(command).strip()

    def get_git_repo_url(self):
        """
        Get current git repo url
        :return: Current git repo url
        """
        return self.get_git_remote().replace('.git', '')
