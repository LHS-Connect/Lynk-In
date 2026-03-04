import subprocess
import re
import json
import os

def get_remote_url():
    try:
        url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode("utf-8").strip()
        url = re.sub(r"git@github\.com:", "https://github.com/", url)
        url = re.sub(r"\.git$", "", url)
        return url
    except:
        return "https://github.com/ChainLynxRobotics/LHS-Connect-Beta"

def update_log():
    remote_base = get_remote_url()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    git_logger_dir = os.path.join(base_dir, "git logger")
    json_path = os.path.join(git_logger_dir, "users.json")
    output_path = os.path.join(git_logger_dir, "git-log-box.txt")

    user_map = {}
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            user_map = json.load(f)

    git_format = "%an|||%s|||%h"
    try:
        raw_log = subprocess.check_output([
            "git", "log",
            f"--pretty=format:{git_format}",
            "--name-only",
            "--invert-grep", "--grep=docs: auto-update git-log-box.txt"
        ]).decode("utf-8")

        commits = raw_log.strip().split("\n\n")
        formatted_lines = []

        for commit in commits:
            lines = commit.strip().split("\n")
            if not lines or not lines[0]: continue
            
            header_parts = lines[0].split("|||")
            if len(header_parts) < 3: continue

            git_name, message, short_hash = header_parts
            files = [l for l in lines[1:] if l.strip()]
            file_str = ", ".join(files[:3]) + (f" (+{len(files)-3} more)" if len(files) > 3 else "")
            
            # Get data from JSON or use defaults
            user_data = user_map.get(git_name, {})
            display_name = user_data.get("display_name", git_name)
            username = user_data.get("username", git_name.replace(" ", ""))
            
            profile_link = f"https://github.com/{username}"
            commit_link = f"{remote_base}/commit/{short_hash}"
            
            # We save the Display Name instead of the raw Git name
            formatted_lines.append(f"{display_name}|||{profile_link}|||{message}|||{file_str}|||{commit_link}")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(formatted_lines))
        print(f"✅ Log fully rebuilt with display names.")
    except Exception as e:
        print(f"❌ Rebuild failed: {e}")

if __name__ == "__main__":
    update_log()