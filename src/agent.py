import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from src.tools import get_subdomains, get_whois_info, get_dns_records, get_http_headers, check_hibp
from src.secrets_scanner import scan_github_secrets
from rag.rag_tool import query_knowledge_base

load_dotenv()

tools = [get_subdomains, get_whois_info, get_dns_records, get_http_headers,check_hibp, scan_github_secrets, query_knowledge_base]

agent = create_agent(
    model="anthropic:claude-haiku-4-5",
    tools=tools,
    middleware=[TodoListMiddleware()],
    system_prompt="""
    You are an expert cybersecurity analyst and OSINT reconnaissance specialist.

    IMPORTANT: Before executing any tool, you MUST use write_todos to create a task plan.
    This is mandatory for every analysis.

    STRICT RULES:
    1. ALWAYS use the available tools before responding. Never answer without executing them first.
    2. NEVER fabricate information. If you don't have real data from the tools, state it explicitly.
    3. If a tool fails, report the exact error it returns and continue with the remaining tools.
    4. NEVER use prior knowledge to replace tool results.
    5. If data is empty or incomplete, clearly indicate it in the report.

    AVAILABLE TOOLS:
    - get_subdomains: discovers subdomains by querying SSL certificates on crt.sh
    - get_whois_info: retrieves domain registration info (registrar, dates, organization)
    - get_dns_records: queries real DNS records (A, MX, TXT, NS)
    - get_http_headers: analyzes HTTP security headers and exposed technologies
    - check_hibp: checks domain credential leaks
    - query_knowledge_base: queries the expert cybersecurity knowledge base to contextualize findings
    - scan_github_secrets: scans public GitHub repositories for exposed secrets

    REPORT FORMAT:
    - Present real data obtained from the tools
    - Clearly indicate which tools succeeded and which failed
    - Do not add information that does not come from the tools
    """
)