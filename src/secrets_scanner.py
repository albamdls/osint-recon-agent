import re
import os
import requests
from langchain.tools import tool

PATRONES = {
    "AWS Access Key": (r"AKIA[0-9A-Z]{16}", "CRÍTICA"),
    "GitHub Token": (r"ghp_[a-zA-Z0-9]{36}", "CRÍTICA"),
    "Anthropic API Key": (r"sk-ant-[a-zA-Z0-9\-]{90,}", "CRÍTICA"),
    "OpenAI API Key": (r"sk-[a-zA-Z0-9]{48}", "CRÍTICA"),
    "Slack Token": (r"xox[baprs]-[0-9a-zA-Z\-]{10,}", "ALTA"),
    "Private Key": (r"-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----", "CRÍTICA"),
    "JWT Token": (r"eyJ[a-zA-Z0-9\-_]+\.eyJ[a-zA-Z0-9\-_]+\.[a-zA-Z0-9\-_]+", "ALTA"),
    "Password hardcodeada": (r"(?i)(password|passwd|pwd)\s*[=:]\s*['\"][^'\"]{4,}['\"]", "ALTA"),
    "Database URL": (r"(?i)(mysql|postgresql|mongodb|redis):\/\/[^\s]+:[^\s]+@[^\s]+", "CRÍTICA"),
    "Generic API Key": (r"(?i)(api[_\-]?key|apikey)\s*[=:]\s*['\"][a-zA-Z0-9\-_]{16,}['\"]", "ALTA"),
    "Stripe Key": (r"sk_live_[a-zA-Z0-9]{24}", "CRÍTICA"),
}

EXTENSIONES_RELEVANTES = {
    ".py", ".js", ".ts", ".env", ".yml", ".yaml",
    ".json", ".sh", ".rb", ".php", ".java", ".go",
    ".cfg", ".ini", ".conf", ".toml"
}

def _ocultar_secreto(texto: str) -> str:
    if len(texto) > 8:
        return texto[:4] + "*" * (len(texto) - 8) + texto[-4:]
    return "****"

def _escanear_contenido(contenido: str, archivo: str) -> list:
    hallazgos = []
    for nombre, (patron, severidad) in PATRONES.items():
        for match in re.finditer(patron, contenido):
            texto = match.group(0)
            hallazgos.append({
                "tipo": nombre,
                "severidad": severidad,
                "valor_parcial": _ocultar_secreto(texto),
                "archivo": archivo,
                "linea": contenido[:match.start()].count("\n") + 1
            })
    return hallazgos

def _obtener_repos(org_o_usuario: str, headers: dict) -> list:
    repos = []
    for tipo in ["users", "orgs"]:
        url = f"https://api.github.com/{tipo}/{org_o_usuario}/repos?per_page=10&sort=updated"
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            repos = response.json()
            break
    return repos

def _escanear_repo(owner: str, repo: str, headers: dict) -> list:
    hallazgos = []
    
    # Obtener árbol de ficheros
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code != 200:
        return hallazgos
    
    tree = response.json().get("tree", [])
    ficheros_relevantes = [
        f for f in tree 
        if f["type"] == "blob" 
        and any(f["path"].endswith(ext) for ext in EXTENSIONES_RELEVANTES)
        and f.get("size", 0) < 100000  # Máximo 100KB
    ][:20]  # Máximo 20 ficheros por repo
    
    for fichero in ficheros_relevantes:
        url_raw = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{fichero['path']}"
        try:
            r = requests.get(url_raw, headers=headers, timeout=10)
            if r.status_code == 200:
                nuevos = _escanear_contenido(r.text, f"{repo}/{fichero['path']}")
                hallazgos.extend(nuevos)
        except:
            pass
    
    return hallazgos

@tool
def escanear_secretos_github(objetivo: str) -> str:
    """
    Escanea repositorios públicos de GitHub en busca de secretos expuestos
    como API keys, tokens, contraseñas hardcodeadas y credenciales.
    El objetivo puede ser un usuario, organización o URL de GitHub.
    Útil para auditar la exposición de credenciales en código público.
    """
    token = os.getenv("GITHUB_TOKEN")
    headers = {"Authorization": f"token {token}"} if token else {}
    headers["Accept"] = "application/vnd.github.v3+json"
    
    # Extraer nombre de usuario/org de la URL si es necesario
    objetivo = objetivo.strip().rstrip("/")
    if "github.com/" in objetivo:
        objetivo = objetivo.split("github.com/")[-1].split("/")[0]
    
    repos = _obtener_repos(objetivo, headers)
    
    if not repos:
        return f"No se encontraron repositorios públicos para: {objetivo}"
    
    todos_hallazgos = []
    repos_escaneados = []
    
    for repo in repos[:5]:  # Máximo 5 repos
        nombre_repo = repo["name"]
        repos_escaneados.append(nombre_repo)
        hallazgos = _escanear_repo(objetivo, nombre_repo, headers)
        todos_hallazgos.extend(hallazgos)
    
    if not todos_hallazgos:
        return f"✅ No se encontraron secretos en los repositorios de {objetivo}.\nRepos escaneados: {', '.join(repos_escaneados)}"
    
    resultado = f"🚨 Se encontraron {len(todos_hallazgos)} posibles secretos en {objetivo}:\n\n"
    resultado += f"Repos escaneados: {', '.join(repos_escaneados)}\n\n"
    
    for h in todos_hallazgos:
        resultado += f"• [{h['severidad']}] {h['tipo']}\n"
        resultado += f"  Archivo: {h['archivo']} (línea {h['linea']})\n"
        resultado += f"  Valor: {h['valor_parcial']}\n\n"
    
    return resultado