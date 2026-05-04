import re
import os
import requests
from langchain.tools import tool

PATTERNS = {
    "AWS Access Key": (r"AKIA[0-9A-Z]{16}", "CRITICAL"),
    "GitHub Token": (r"ghp_[a-zA-Z0-9]{36}", "CRITICAL"),
    "Anthropic API Key": (r"sk-ant-[a-zA-Z0-9\-]{90,}", "CRITICAL"),
    "OpenAI API Key": (r"sk-[a-zA-Z0-9]{48}", "CRITICAL"),
    "Slack Token": (r"xox[baprs]-[0-9a-zA-Z\-]{10,}", "HIGH"),
    "Private Key": (r"-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----", "CRITICAL"),
    "JWT Token": (r"eyJ[a-zA-Z0-9\-_]+\.eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+", "HIGH"),
    "Hardcoded Password": (r"(?i)(password|passwd|pwd)\s*[=:]\s*['\"][^'\"]{4,}['\"]", "HIGH"),
    "Database URL": (r"(?i)(mysql|postgresql|mongodb|redis):\/\/[^\s]+:[^\s]+@[^\s]+", "CRITICAL"),
    "Generic API Key": (r"(?i)(api[_\-]?key|apikey)\s*[=:]\s*['\"][a-zA-Z0-9\-_]{16,}['\"]", "HIGH"),
    "Stripe Key": (r"sk_live_[a-zA-Z0-9]{24}", "CRITICAL"),
}

RELEVANT_EXTENSIONS = {
    ".py", ".js", ".ts", ".env", ".yml", ".yaml",
    ".json", ".sh", ".rb", ".php", ".java", ".go",
    ".cfg", ".ini", ".conf", ".toml"
}

def _mask_secret(text: str) -> str:
    if len(text) > 8:
        return text[:4] + "*" * (len(text) - 8) + text[-4:]
    return "****"

def _scan_content(content: str, file: str) -> list:
    findings = []
    for name, (pattern, severity) in PATTERNS.items():
        for match in re.finditer(pattern, content):
            text = match.group(0)
            findings.append({
                "type": name,
                "severity": severity,
                "partial_value": _mask_secret(text),
                "file": file,
                "line": content[:match.start()].count("\n") + 1
            })
    return findings

def _get_repos(user_or_org: str, headers: dict) -> list:
    repos = []
    for tipo in ["users", "orgs"]:
        url = f"https://api.github.com/{tipo}/{user_or_org}/repos?per_page=10&sort=updated"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            repos = response.json()
            break
    return repos

def _scan_repo(owner: str, repo: str, headers: dict) -> list:
    findings = []
    
    # Get file tree
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        return findings
    
    tree = response.json().get("tree", [])
    relevant_files = [
        f for f in tree 
        if f["type"] == "blob" 
        and any(f["path"].endswith(ext) for ext in RELEVANT_EXTENSIONS)
        and f.get("size", 0) < 100000  # Max 100KB
    ][:20]  # Max 20 files per repo
    
    for file in relevant_files:
        url_raw = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{file['path']}"
        try:
            r = requests.get(url_raw, headers=headers, timeout=10)
            if r.status_code == 200:
                new_findings = _scan_content(r.text, f"{repo}/{file['path']}")
                findings.extend(new_findings)
        except:
            pass
    
    return findings

@tool
def scan_github_secrets(target: str) -> str:
    """
    Scans public GitHub repositories for exposed secrets
    such as API keys, tokens, hardcoded passwords, and credentials.
    The target can be a user, organization, or GitHub URL.
    Useful for auditing credential exposure in public code.
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    headers["Accept"] = "application/vnd.github.v3+json"
    
    # Extract username/org from URL if needed
    target = target.strip().rstrip("/")
    if "github.com/" in target:
        target = target.split("github.com/")[-1].split("/")[0]
    
    repos = _get_repos(target, headers)
    
    if not repos:
        return f"No public repositories found for: {target}"
    
    all_findings = []
    scanned_repos = []
    
    for repo in repos[:5]:  # Max 5 repos
        repo_name = repo["name"]
        scanned_repos.append(repo_name)
        findings = _scan_repo(target, repo_name, headers)
        all_findings.extend(findings)
    
    if not all_findings:
        return f"✅ No secrets found in {target}'s repositories.\nScanned repos: {', '.join(scanned_repos)}"
    
    result = f"🚨 Found {len(all_findings)} possible secrets in {target}:\n\n"
    result += f"Scanned repos: {', '.join(scanned_repos)}\n\n"
    
    for f in all_findings:
        result += f"• [{f['severity']}] {f['type']}\n"
        result += f"  File: {f['file']} (line {f['line']})\n"
        result += f"  Value: {f['partial_value']}\n\n"
    
    return result