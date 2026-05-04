import os
import requests
import whois
import time
import dns.resolver

from langchain.tools import tool

@tool
def get_subdomains(domain: str):
    """
    Retrieves a list of subdomains for a given domain by querying
    public SSL certificates on crt.sh.
    """
    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        headers = {"User-Agent": "Mozilla/5.0"}

        for attempt in range(3):
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200 and response.text.strip():
                break
            time.sleep(2)

        data = response.json()
        subdomains = []
        for x in data:
            subdomains.append(x["name_value"])

        # set() removes duplicates, list() converts it back to a list
        return list(set(subdomains))
    except Exception as e:
        return f"Error querying crt.sh: {str(e)}"


@tool
def get_whois_info(domain: str):
    """
    Queries public domain registration databases and returns information
    such as who registered the domain, registration and expiration dates,
    DNS servers, and registrant contact data.
    """
    whois_data = {}

    try:
        result = whois.whois(domain)
        whois_data = {
            "domain_name": result["domain_name"],
            "registrar": result["registrar"],
            "creation_date": result["creation_date"],
            "expiration_date": result["expiration_date"],
            "country": result["country"],
            "org": result["org"],
            "name_servers": result["name_servers"]
        }
    except Exception as e:
        print(f"Error using whois tool: {str(e)}")

    return whois_data


@tool
def get_dns_records(domain: str):
    """
    Queries DNS records for a given domain.
    Returns A (IPs), MX (mail servers), TXT (verifications and policies)
    and NS (DNS servers) records.
    Useful for mapping the domain's infrastructure and services.
    """
    records = {
        "A": [],
        "MX": [],
        "TXT": [],
        "NS": []
    }

    try:
        for record in dns.resolver.resolve(domain, "A"):
            records["A"].append(str(record))
    except Exception as e:
        print(f"Error on A: {e}")

    try:
        for record in dns.resolver.resolve(domain, "MX"):
            records["MX"].append(str(record))
    except Exception as e:
        print(f"Error on MX: {e}")

    try:
        for record in dns.resolver.resolve(domain, "TXT"):
            records["TXT"].append(str(record))
    except Exception as e:
        print(f"Error on TXT: {e}")

    try:
        for record in dns.resolver.resolve(domain, "NS"):
            records["NS"].append(str(record))
    except Exception as e:
        print(f"Error on NS: {e}")

    return records


@tool
def get_http_headers(domain: str):
    """
    Analyzes HTTP security headers of a domain.
    Detects present and missing security headers, and exposed technologies.
    Useful for evaluating the web security level of the target.
    """
    try:
        url = f"https://{domain}"
        headers_request = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers_request, timeout=10, allow_redirects=True)

        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Frame-Options",
            "X-Content-Type-Options",
            "Referrer-Policy",
            "Permissions-Policy"
        ]

        result = {
            "status_code": response.status_code,
            "server": response.headers.get("Server", "Not exposed"),
            "x_powered_by": response.headers.get("X-Powered-By", "Not exposed"),
            "security_headers_present": [],
            "security_headers_missing": []
        }

        for header in security_headers:
            if header in response.headers:
                result["security_headers_present"].append(header)
            else:
                result["security_headers_missing"].append(header)

        return result
    except Exception as e:
        return f"Error analyzing headers for {domain}: {str(e)}"


@tool
def check_hibp(domain: str):
    """
    Checks whether emails from the domain have appeared in data breaches.
    Uses HaveIBeenPwned if an API key is configured, or LeakCheck as a free alternative.
    Useful for evaluating the credential exposure risk of a domain.
    """
    try:
        hibp_api_key = os.getenv("HIBP_API_KEY")

        if hibp_api_key:
            headers = {
                "hibp-api-key": hibp_api_key,
                "User-Agent": "osint-recon-agent"
            }
            url = f"https://haveibeenpwned.com/api/v3/breacheddomain/{domain}"
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return {
                    "source": "HaveIBeenPwned",
                    "domain": domain,
                    "compromised_emails": len(data),
                    "details": data
                }
            elif response.status_code == 404:
                return {"source": "HaveIBeenPwned", "domain": domain, "result": "No breaches found"}
            else:
                return f"HIBP error: status code {response.status_code}"

        else:
            url = f"https://leakcheck.io/api/public?check={domain}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                return {
                    "source": "LeakCheck (free alternative)",
                    "domain": domain,
                    "result": data
                }
            else:
                return f"LeakCheck error: status code {response.status_code}"

    except Exception as e:
        return f"Error checking credential leaks: {str(e)}"