import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from src.schemas import ReconReport, WhoisInfo, DNSInfo, HeadersInfo, BreachesInfo
from src.tools import get_subdomains, get_whois_info, get_dns_records, get_http_headers, check_hibp
from datetime import datetime

load_dotenv()

llm = ChatAnthropic(model="claude-haiku-4-5-20251001")
llm_structured = llm.with_structured_output(ReconReport)

def analyze_domain_structured(domain: str) -> ReconReport:
    """
    Runs OSINT tools and returns a structured report
    using Pydantic to guarantee the output format.
    """
    # 1. Run tools directly
    results = {}
    failed_tools = []

    try:
        results["whois"] = get_whois_info.invoke({"domain": domain})
    except Exception as e:
        failed_tools.append(f"whois: {str(e)}")

    try:
        results["dns"] = get_dns_records.invoke({"domain": domain})
    except Exception as e:
        failed_tools.append(f"dns: {str(e)}")

    try:
        results["subdomains"] = get_subdomains.invoke({"domain": domain})
    except Exception as e:
        failed_tools.append(f"subdomains: {str(e)}")

    try:
        results["headers"] = get_http_headers.invoke({"domain": domain})
    except Exception as e:
        failed_tools.append(f"headers: {str(e)}")

    try:
        results["breaches"] = check_hibp.invoke({"domain": domain})
    except Exception as e:
        failed_tools.append(f"breaches: {str(e)}")

    # 2. Ask the LLM to structure the data
    prompt = f"""
    Analyze the following OSINT data for the domain {domain} and return a structured report.
    
    Collected data:
    {results}
    
    Failed tools: {failed_tools}
    
    Fill in all schema fields with the available information.
    For risk_level use: LOW, MEDIUM, HIGH or CRITICAL.
    For summary write 2-3 sentences summarizing the most important findings.
    For recommendations list the 3-5 most important ones.
    """

    report = llm_structured.invoke(prompt)
    report.domain = domain
    report.analysis_date = datetime.now().strftime("%d/%m/%Y %H:%M")
    report.failed_tools = failed_tools

    return report