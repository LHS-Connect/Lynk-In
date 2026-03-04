import subprocess
import re
import json
import os

FOLDER_NAME = "git logger"

def get_remote_url():
    try:
        url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode("utf-8").strip()
        url = re.sub(r"git@github\.com:", "https://github.com/", url)
        url = re.sub(r"\.git$", "", url)
        return url
    except:
        return "https://github.com/LHS-Connect/Lynk-In"

def update_log():
    remote_base = get_remote_url()

    user_map = {}
    git_logger_dir = os.path.join(os.path.dirname(__file__), "git logger")
    json_path = os.path.join(git_logger_dir, "users.json")
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            user_map = json.load(f)

    git_format = "%an|||%s|||%h"
    try:
        raw_log = subprocess.check_output([
            "git", "log",
            f"--pretty=format:{git_format}",
            "--name-only"
        ]).decode("utf-8")

        commits = raw_log.split("\n\n")
        formatted_lines = []

        for commit in commits:
            lines = commit.strip().split("\n")
            if not lines or not lines[0]:
                continue
            header_parts = lines[0].split("|||")
            if len(header_parts) < 3:
                continue

            author, message, short_hash = header_parts
            files = [l for l in lines[1:] if l.strip()]
            file_str = ", ".join(files[:3]) + (f" (+{len(files)-3} more)" if len(files) > 3 else "")
            username = user_map.get(author, author.replace(" ", ""))
            profile_link = f"https://github.com/{username}"
            commit_link = f"{remote_base}/commit/{short_hash}"
            formatted_lines.append(f"{author}|||{profile_link}|||{message}|||{file_str}|||{commit_link}")

        output_path = os.path.join(git_logger_dir, "git-log-box.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(formatted_lines))

        print(f"✅  git-log-box.txt updated ({len(formatted_lines)} commits)")
        return output_path

    except Exception as e:
        print(f"❌  Log update failed: {e}")
        return None

def make_commit():
    print("\n📝  Prepare your commit message:")
    
    # Prompting for specific details
    change = input("What is being updated? :: ").strip()
    reason = input("Why is it being updated? :: ").strip()

    if not change or not reason:
        print("❌  Both fields are required for the commit message.")
        return

    # Formatting the message
    full_message = f"Changed :: {change} | Reason :: {reason}"

    try:
        # Stage all of the files
        subprocess.check_call(["git", "add", "-A"])
        print("✅  Staged all files.")

        # Make the commit with the formatted message
        subprocess.check_call(["git", "commit", "-m", full_message])
        print(f"✅  Commit made: {full_message}")

        # Rewrite the log now that the commit exists in history
        log_path = update_log()

        if log_path:
            # Stage the updated log file and amend it into the commit
            subprocess.check_call(["git", "add", log_path])
            subprocess.check_call(["git", "commit", "--amend", "--no-edit"])
            print("✅  git-log-box.txt amended into commit.")

    except subprocess.CalledProcessError as e:
        print(f"❌  Git command failed: {e}")

if __name__ == "__main__":
    make_commit()