# OSINT AI CLI 🔍

> AI-powered OSINT reconnaissance tool developed as the Final Project for the Automation and Process Optimization course.

**⚠️ FOR ACADEMIC AND EDUCATIONAL USE ONLY. Unauthorized use against third-party systems is illegal.**

---

## 📋 Description

OSINT AI CLI is a terminal application that combines **Open Source Intelligence (OSINT)** techniques with **Artificial Intelligence** to automate domain reconnaissance. The agent autonomously orchestrates multiple tools, reasons about results, and generates structured reports with expert cybersecurity context.

### What can it do?

- 🌐 Discover subdomains via public SSL certificates (crt.sh)
- 📋 Retrieve domain registration information (WHOIS)
- 🔗 Analyze DNS records (A, MX, TXT, NS)
- 🔒 Evaluate HTTP security headers
- ⚠️ Check credential leaks (LeakCheck)
- 🔍 Scan public GitHub repositories for exposed secrets
- 📚 Contextualize findings with an expert knowledge base (RAG)
- 🎯 Automatically calculate risk scores
- 📄 Export reports to PDF

---

## 🏗️ Architecture
```bash
osint-recon-agent/
├── main.py                    # Main CLI with Rich + questionary
├── src/
│   ├── agent.py               # LangChain agent with TodoListMiddleware
│   ├── tools.py               # OSINT tools (crt.sh, WHOIS, DNS, HTTP, HIBP)
│   ├── secrets_scanner.py     # GitHub secrets scanner
│   ├── structured_agent.py    # Agent with Pydantic structured output
│   ├── schemas.py             # Pydantic ReconReport schema
│   └── scorer.py              # Risk scoring system
├── rag/
│   ├── indexer.py             # Document indexing into ChromaDB
│   ├── retriever.py           # Semantic search
│   ├── rag_tool.py            # RAG tool for the agent
│   └── data/                  # Knowledge base in markdown
│       ├── http_security_headers.md
│       ├── owasp_top10.md
│       ├── dns_registros.md
│       ├── filtraciones_datos.md
│       └── subdominios_osint.md
├── reports/
│   └── pdf_generator.py       # PDF report generator
├── notebooks/
│   └── evaluacion_baseline.ipynb  # Evaluation and model comparison
├── docs/                      # Evaluation charts
├── informes/                  # Generated PDFs
└── requirements.txt
```

---

## 🚀 Installation

### Prerequisites
- Python 3.11+
- Fedora/Linux (recommended) or Windows/macOS

### 1. Clone the repository

```bash
git clone https://github.com/albamdls/osint-recon-agent.git
cd osint-recon-agent
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# or on Windows:
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
ANTHROPIC_API_KEY=your_api_key_here
GITHUB_TOKEN=your_github_token_here  # optional, improves rate limit
```

### 5. Initialize the RAG knowledge base

```bash
python3 rag/indexer.py
```

### 6. Run the application

```bash
python -m main
```

---

## 🔑 Required API Keys

| Service | Required | Cost | Get it at |
|---------|----------|------|-----------|
| Anthropic | ✅ Yes | ~$5 for the full project | [console.anthropic.com](https://console.anthropic.com) |
| GitHub Token | ⚠️ Recommended | Free | GitHub → Settings → Developer settings |

---

## 🛠️ Implemented Tools

| Tool | Source | Description |
|------|--------|-------------|
| `get_subdomains` | crt.sh | Subdomain discovery via SSL certificates |
| `get_whois_info` | python-whois | Domain registration information |
| `get_dns_records` | dnspython | DNS records (A, MX, TXT, NS) |
| `get_http_headers` | requests | HTTP security headers analysis |
| `check_hibp` | LeakCheck | Credential leak verification |
| `escanear_secretos_github` | GitHub API | Secrets scanner in public repositories |
| `consultar_base_conocimiento` | ChromaDB + HuggingFace | RAG with expert cybersecurity knowledge |

---

## 📊 Evaluation

The notebook `notebooks/evaluacion_baseline.ipynb` documents:

- **Baseline**: agent performance metrics (tokens, cost, time)
- **Manual vs agent comparison**: the agent is ~38x faster
- **Structured output**: evaluation with Pydantic
- **Model comparison**: Claude Haiku vs Claude Sonnet

### Key Results

| Metric | Value |
|--------|-------|
| Average analysis time | ~25s |
| Average cost per analysis | $0.013 |
| Speed vs manual search | 38x faster |
| Quality score | 4.7/5 |
| Optimal model | Claude Haiku (best cost/quality ratio) |

---

## 🧠 Tech Stack

- **LLM**: Claude Haiku via Anthropic API
- **Agent framework**: LangChain 1.x with `create_agent`
- **Middleware**: `TodoListMiddleware` for task planning
- **RAG**: ChromaDB + sentence-transformers (all-MiniLM-L6-v2)
- **Structured output**: Pydantic BaseModel
- **CLI**: Rich + questionary + pyfiglet
- **PDF**: fpdf2 + DejaVu fonts

---

## 📝 Usage

### Full domain analysis
``` 
python -m main
→ ⚡ Full analysis
→ Enter domain: example.com
``` 

### Custom analysis
``` 
python -m main
→ 🔧 Custom analysis
→ Select tools with spacebar
→ Enter domain
``` 

### Scan secrets in GitHub
``` 
python -m main
→ 🔍 Scan secrets in GitHub
→ Enter user or organization: username
``` 

---

## ⚠️ Known Limitations

- **crt.sh**: public API with rate limiting — may fail intermittently
- **LeakCheck**: free alternative to HIBP with less data
- **GitHub scanner**: scans maximum 5 repos and 20 files per repo
- **Local models**: Ollama available as an alternative without API key

---

## 👩‍💻 Author

**Alba Mora de la Sen** — Final Project, AI Automation and Process Optimization 2026

---

## 📚 References

- [LangChain Documentation](https://docs.langchain.com)
- [Anthropic API](https://docs.anthropic.com)
- [OWASP Top 10](https://owasp.org/Top10/)
- [crt.sh Certificate Transparency](https://crt.sh)
- [HaveIBeenPwned](https://haveibeenpwned.com)
- [Google Prompting Whitepaper](https://ai.google.dev/responsible/docs/advanced_responsible_ai_handbook)