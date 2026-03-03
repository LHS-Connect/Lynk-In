import subprocess
import re
import http.server
import socketserver
import webbrowser
import threading
import json
import os

# Configuration: Update this if your folder name changes
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
    
    # Load user mappings from the current folder
    user_map = {}
    json_path = os.path.join(os.path.dirname(__file__), 'users.json')
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            user_map = json.load(f)

    git_format = "%an|||%s|||%h"
    
    try:
        raw_log = subprocess.check_output([
            "git", "log", 
            f"--pretty=format:{git_format}", 
            "--name-only"
        ]).decode("utf-8")
        
        commits = raw_log.split('\n\n')
        formatted_lines = []
        
        for commit in commits:
            lines = commit.strip().split('\n')
            if not lines or not lines[0]: continue
            
            header_parts = lines[0].split('|||')
            if len(header_parts) < 3: continue
            author, message, short_hash = header_parts
            
            files = lines[1:]
            file_str = ", ".join(files[:3]) + (f" (+{len(files)-3} more)" if len(files) > 3 else "")
            
            username = user_map.get(author, author.replace(" ", ""))
            profile_link = f"https://github.com/{username}"
            commit_link = f"{remote_base}/commit/{short_hash}"
            
            formatted_lines.append(f"{author}|||{profile_link}|||{message}|||{file_str}|||{commit_link}")
            
        output_path = os.path.join(os.path.dirname(__file__), "git-log-box.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(formatted_lines))
        print(f"✅ Log updated in {FOLDER_NAME}/git-log-box.txt")
            
    except Exception as e:
        print(f"Update failed: {e}")
