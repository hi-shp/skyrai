import os
import sys
import time
import subprocess
import datetime

# Fix Windows console UTF-8 output
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# ═══════════════════════════════════════════════════════════════
# SKYRAI Auto Git Sync Daemon
# Automatically tracks file edits in c:\ihm, generates meaningful
# commit messages, and pushes to https://github.com/hi-shp/skyrai.git
# ═══════════════════════════════════════════════════════════════

WATCH_DIR = os.path.dirname(os.path.abspath(__file__))
CHECK_INTERVAL_SECONDS = 3

def run_cmd(cmd_list):
    try:
        res = subprocess.run(
            cmd_list,
            cwd=WATCH_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        return res.returncode, res.stdout.strip(), res.stderr.strip()
    except Exception as e:
        return 1, "", str(e)

def get_git_status():
    code, out, _ = run_cmd(["git", "status", "--porcelain"])
    if code != 0 or not out:
        return []
    lines = [l.strip() for l in out.splitlines() if l.strip()]
    return lines

def generate_commit_message(status_lines):
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    changed_files = []
    actions = []
    
    for line in status_lines:
        status_code = line[:2].strip()
        filepath = line[2:].strip()
        filename = os.path.basename(filepath)
        changed_files.append(filename)
        
        if 'M' in status_code:
            actions.append(f"update {filename}")
        elif 'A' in status_code or '?' in status_code:
            actions.append(f"add {filename}")
        elif 'D' in status_code:
            actions.append(f"remove {filename}")

    distinct_files = list(dict.fromkeys(changed_files))
    
    if "skyrai.html" in distinct_files or "1.html" in distinct_files:
        summary = "feat: Update SKYRAI frontend & precision analytics"
    elif "server.py" in distinct_files:
        summary = "fix: Update backend Sentinel Hub API integration"
    elif ".env" in distinct_files:
        summary = "chore: Update configuration & API keys"
    elif "README.md" in distinct_files:
        summary = "docs: Update project documentation"
    else:
        summary = f"sync: Auto-sync {', '.join(distinct_files[:3])}"

    details = "; ".join(actions[:5])
    return f"{summary} ({details} at {now_str})"

def main():
    print(f"🚀 SKYRAI Auto-Git-Sync daemon active on {WATCH_DIR}...")
    
    while True:
        try:
            status_lines = get_git_status()
            if status_lines:
                # Wait 1 extra second for write completion
                time.sleep(1)
                status_lines = get_git_status()
                if status_lines:
                    msg = generate_commit_message(status_lines)
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Detected changes: {status_lines}")
                    
                    # 1. git add
                    run_cmd(["git", "add", "-A"])
                    
                    # 2. git commit
                    c_code, c_out, c_err = run_cmd(["git", "commit", "-m", msg])
                    if c_code == 0:
                        print(f"✓ Committed: {msg}")
                        # 3. git push
                        p_code, p_out, p_err = run_cmd(["git", "push", "origin", "main"])
                        if p_code == 0:
                            print(f"✓ Successfully pushed to GitHub (origin/main)!")
                        else:
                            print(f"⚠️ Push error: {p_err}")
                    else:
                        print(f"⚠️ Commit skip: {c_out or c_err}")
                        
        except Exception as e:
            print(f"⚠️ Sync exception: {e}")
            
        time.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
