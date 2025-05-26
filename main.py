# git remote set-url origin git@github.com:Mattyh357/DotHermit.git

import os
import socket
import hashlib
import shutil
import subprocess
import configparser
from pathlib import Path
import sys
import difflib



# === CONFIG ===
REPO_PATH = os.path.expanduser("~/Dropbox/0Repos/Python/DotHermit/")
REPO_DOTS = REPO_PATH + "dot_files/"


# === HELPERS ===
def get_hostname():
	return socket.gethostname()




class GitHubHandler:
    def __init__(self, repo_path='.'):
        self.repo_path = repo_path

    def _run_git(self, args):
        try:
            result = subprocess.run(
                ['git'] + args,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Git command failed: {' '.join(args)}\n{e.stderr.strip()}")

    def is_git_installed(self):
        try:
            output = subprocess.run(['git', '--version'], capture_output=True, text=True, check=True)
            return output.stdout.strip().startswith('git version')
        except Exception:
            return False

    def check_for_updates(self):
        # Fetch remote info
        self._run_git(['fetch'])
        status = self._run_git(['status', '-uno'])
        if "behind" in status:
            return True
        return False

    def pull_updates(self):
        return self._run_git(['pull'])

    def stage_all_changes(self):
        return self._run_git(['add', 'dot_files'])

    def commit_changes(self, message):
        return self._run_git(['commit', '-m', message])

    def push_changes(self):
        return self._run_git(['push'])




class ConfigHelper:
    def __init__(self, ini_path):
        self.ini_path = os.path.expanduser(ini_path)
        self.config = configparser.ConfigParser()
        self.config.read(self.ini_path)

    def get_hosts(self):
        # Returns dict of hostname mappings from [hosts]
        if 'hosts' not in self.config:
            return {}
        return dict(self.config['hosts'])

    def get_all_files(self):
        # Returns list of all files (full expanded paths)
        if 'files' not in self.config:
            return {}

        all_files = {}
        for path, perm in self.config['files'].items():
            expanded_path = os.path.expanduser(path)
            p = Path(expanded_path)
            if p.is_dir():
                # TODO error handling - directory
                pass
            else:
                all_files[path] = perm

        return all_files


def copy_file(path_local, path_repo):
    try:
        path_repo.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path_local, path_repo)

        # Optional verification
        if path_local.stat().st_size == path_repo.stat().st_size:
            return True
        else:
            print(f"Warning: Size mismatch after copying '{path_local}' to '{path_repo}'")
            return False

    except Exception as e:
        print(f"Error copying '{path_local}' to '{path_repo}': {e}")
        return False




def file_compare(p_local, p_repo):
    """
    Compare two files and return:
    0  => same (hash matches)
    -1 => missing (one or both files missing)
    1  => different (files differ)
    """

    # TODO change to bool and throw error on missing

    if not p_local.exists() or not p_repo.exists():
        if not p_local.exists():
            print("not p_local.exists()")
        if not p_repo.exists():
            print("remo mossing: ", p_repo)
        return -1  # missing

    def file_hash(p):
        h = hashlib.sha256()
        with p.open('rb') as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    hash_local = file_hash(p_local)
    hash_repo = file_hash(p_repo)

    if hash_local == hash_repo:
        return 0
    else:
        return 1

def side_by_side_diff(file1, file2, width=60):
    with open(file1) as f1, open(file2) as f2:
        lines1 = [line.rstrip('\n') for line in f1]
        lines2 = [line.rstrip('\n') for line in f2]

    max_lines = max(len(lines1), len(lines2))
    lines1 += [''] * (max_lines - len(lines1))
    lines2 += [''] * (max_lines - len(lines2))

    print(f"{'Local file'.ljust(width)} | {'Repo file'.ljust(width)}")
    print("-" * (width * 2 + 3))

    for left, right in zip(lines1, lines2):
        print(f"{left.ljust(width)} | {right.ljust(width)}")

def check_dot_files():
    repo_changed = False

    ch = ConfigHelper('config.ini')  # TODO magic
    files = ch.get_all_files()

    print("Comparing Dot files:")

    for path_local, perm in files.items():
        # Get full paths
        p_local = Path(os.path.expanduser(path_local)).resolve()

        home = Path.home().resolve()
        try:
            relative_path = p_local.relative_to(home)
        except ValueError:
            raise ValueError(f"Source path {p_local} is not inside home directory {home}")

        p_repo = p_repo = Path(REPO_DOTS).resolve() / relative_path


        # Create empty file if it doesn't exist
        if not p_local.exists():
            # create empty file if source missing
            p_local.touch()
            print(f"Warning: file '{path_local}' was missing LOCALLY.'")
        if not p_repo.exists():
            # create empty file if source missing
            p_repo.touch()
            print(f"Warning: file '{p_repo}' was missing IN REPO.'")


        compare_result = file_compare(p_local, p_repo)

        if compare_result == 0:
            print("[SAME]", path_local)

        elif compare_result == -1:
            # TODO this should actually throw an error
            print("[NEW FILE]", path_local)
            if copy_file(p_local, p_repo):
                print(f" >> [FILE ADDED] {path_local} copied to repo")
            else:
                print(f"[!] Failed to copy {path_local}")
                exit(1)

        else:
            option = ""
            while option not in ("R", "L", "I"):
                print("-----------------")
                print("[DIFFERENT]", path_local)
                print("(S) Show files side by side")
                print("(L) keep left side (local file)")
                print("(R) keep right side (repo file)")
                print("(I) ignore this file for now")
                option = input("What to do? ")

                if option == "S":
                    side_by_side_diff(p_local, p_repo)
                elif option == "L":
                    pass
                    copy_file(p_local, p_repo)
                    repo_changed = True
                elif option == "R":
                    copy_file(p_repo, p_local)
                    pass
                elif option == "I":
                    pass
    # Done
    return repo_changed


# === MAIN ===
if __name__ == "__main__":

    git_handler = GitHubHandler(REPO_PATH)

    if not git_handler.is_git_installed():
        print("Git is not installed!")
        exit(1)

    # Pull latest repo
    # if git_handler.check_for_updates():
    #     print("Updates are available. Pulling...")
    #     # print(handler.pull_updates())
    #     # TODO error handling

	# Check dot files
    repo_changed = check_dot_files()


    # Push changes
    if repo_changed:
        option = ""
        while option not in ("Y", "N"):
            print("##################")
            print("Files ir repo were changed. would you like to push the changes to git?")
            option = input("Push (Y/N):")

            if option == "Y":
                message = input("Enter commit message: ")
                # push
                git_handler.stage_all_changes()
                git_handler.commit_changes(message)
                git_handler.push_changes()


# TODO force push arg
# TODO force pull
# TODO help argument
# TODO Create directory when touch new file
