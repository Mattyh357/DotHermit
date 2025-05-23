# dotdeploy core starter
# git remote set-url origin git@github.com:Mattyh357/DotHermit.git
from xml.etree.ElementInclude import include

# TODO fix
import os
PROJECT_PATH = os.path.expanduser("~/Dropbox/0Repos/Python/DotHermit/")

import socket
import hashlib
from pathlib import Path

# === CONFIG ===
# Hardcoded test list of files/dirs to track
TRACKED_PATHS = [
	"~/.zshrc",
	"~/.xsessionrc",
	"~/.config/i3",
	"~/.config/polybar",
]

# === HELPERS ===
def get_hostname():
	return socket.gethostname()

def resolve_path(path):
	return Path(os.path.expanduser(path)).resolve()

def file_hash(path):
	try:
		with open(path, 'rb') as f:
			return hashlib.sha256(f.read()).hexdigest()
	except Exception as e:
		return f"ERR:{e}"

def print_tracked_info():
	hostname = get_hostname()
	print(f"Hostname: {hostname}\n")

	for item in TRACKED_PATHS:
		resolved = resolve_path(item)
		if resolved.is_file():
			print(f"File: {resolved}")
			h = file_hash(resolved)
			print(f"  Hash: {h}\n")
		elif resolved.is_dir():
			print(f"Directory: {resolved}")
			for sub in sorted(resolved.rglob("*")):
				if sub.is_file():
					h = file_hash(sub)
					print(f"  - {sub.relative_to(resolved)}  ::  {h}")
			print()
		else:
			print(f"Missing: {resolved}\n")


import subprocess





from GitHelper import GitHubHandler



#tets
# === MAIN ===
if __name__ == "__main__":
	handler = GitHubHandler(PROJECT_PATH)

	if not handler.is_git_installed():
		print("Git is not installed!")
		exit(1)

	if handler.check_for_updates():
		print("Updates are available. Pulling...")
		# print(handler.pull_updates())
	else:
		print("No updates found.")

	# To upload:
	# handler.stage_all_changes()
	# handler.commit_changes("Your commit message")
	# handler.push_changes()



