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
    
    # Pathing relative to the script location
    base_dir = os.path.dirname(os.path.abspath(__file__))
    git_logger_dir = os.path.join(base_dir, "git logger")
    json_path = os.path.join(git_logger_dir, "users.json")
    output_path = os.path.join(git_logger_dir, "git-log-box.txt")

    # Load User Mapping
    user_map = {}
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            user_map = json.load(f)

    # Git format: Author ||| Message ||| Short Hash
    git_format = "%an|||%s|||%h"
    
    try:
        # We fetch the FULL log. --invert-grep hides the bot's own update commits
        raw_log = subprocess.check_output([
            "git", "log",
            f"--pretty=format:{git_format}",
            "--name-only",
            "--invert-grep", 
            "--grep=docs: auto-update git-log-box.txt"
        ]).decode("utf-8")

        # Split by double newline (standard output of --name-only)
        commits = raw_log.strip().split("\n\n")
        formatted_lines = []

        for commit in commits:
            lines = commit.strip().split("\n")
            if not lines or not lines[0]: continue
            
            header_parts = lines[0].split("|||")
            if len(header_parts) < 3: continue

            author, message, short_hash = header_parts
            
            # Extract changed files (lines after the header)
            files = [l for l in lines[1:] if l.strip()]
            file_str = ", ".join(files[:3]) + (f" (+{len(files)-3} more)" if len(files) > 3 else "")
            
            # Map the author to the GitHub username/profile
            user_info = user_map.get(author)
            if isinstance(user_info, dict):
                username = user_info.get("username", author.replace(" ", ""))
            else:
                username = author.replace(" ", "")
            
            profile_link = f"https://github.com/{username}"
            commit_link = f"{remote_base}/commit/{short_hash}"
            
            # Construct the line for the TXT file
            formatted_lines.append(f"{author}|||{profile_link}|||{message}|||{file_str}|||{commit_link}")

        # Write (Full Replace)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(formatted_lines))

        print(f"✅ Log fully rebuilt: {len(formatted_lines)} entries.")
    except Exception as e:
        print(f"❌ Rebuild failed: {e}")

if __name__ == "__main__":
    update_log()