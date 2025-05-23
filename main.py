# dotdeploy core starter

import os
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

def check_for_updates():
    try:
        # Fetch latest changes (no merge)
        subprocess.run(["git", "fetch"], check=True)

        # Check if local is behind
        result = subprocess.run(
            ["git", "status", "-uno"],
            capture_output=True,
            text=True
        )

        if "Your branch is behind" in result.stdout:
            print("A newer version of DotDeploy is available.")
            print("Run: git pull")
        else:
            print("DotDeploy is up to date.")
    except Exception as e:
        print(f"Error checking updates: {e}")



# === MAIN ===
if __name__ == "__main__":
	check_for_updates()
	# print_tracked_info()