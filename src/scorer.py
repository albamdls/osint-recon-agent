from src.schemas import ReconReport

def calculate_score(report: ReconReport) -> dict:
    """
    Calculates a risk score based on the findings in the report.
    Returns numeric score and risk level.
    """
    score = 0
    details = []

    # WHOIS
    if report.whois:
        if report.whois.registrar:
            score -= 5
            details.append(("✅ Professional registrar", -5))

    # HTTP Headers
    if report.headers:
        critical_headers = {
            "Content-Security-Policy": 25,
            "Strict-Transport-Security": 20,
            "X-Frame-Options": 15,
            "X-Content-Type-Options": 10,
            "Referrer-Policy": 5,
            "Permissions-Policy": 5
        }
        for header, points in critical_headers.items():
            if header in report.headers.missing_headers:
                score += points
                details.append((f"❌ {header} missing", +points))
            else:
                score -= round(points * 0.3)
                details.append((f"✅ {header} present", -round(points * 0.3)))

    # Data breaches
    if report.breaches:
        total = report.breaches.total_records
        if total == 0:
            score -= 10
            details.append(("✅ No breaches detected", -10))
        elif total < 10:
            score += 10
            details.append((f"⚠️ {total} breaches", +10))
        elif total < 100:
            score += 20
            details.append((f"⚠️ {total} breaches", +20))
        elif total < 1000:
            score += 35
            details.append((f"🚨 {total} breaches", +35))
        else:
            score += 50
            details.append((f"🚨 +1000 breaches", +50))

    # Sensitive subdomains
    risky_subdomains = ["admin", "staging", "dev", "test", "vpn", "jenkins", "jira"]
    if report.subdomains:
        found = [s for s in report.subdomains 
                 if any(r in s.lower() for r in risky_subdomains)]
        if found: 
            score += len(found) * 5
            details.append((f"⚠️ {len(found)} sensitive subdomains", +len(found)*5))

    # Failed tools
    if report.failed_tools:
        score += len(report.failed_tools) * 3
        details.append((f"⚠️ {len(report.failed_tools)} failed tools", 
                        +len(report.failed_tools)*3))

    # Calculate level
    if score <= 10:
        level = "LOW"
        color = "green"
    elif score <= 30:
        level = "MEDIUM"
        color = "yellow"
    elif score <= 60:
        level = "HIGH"
        color = "orange"
    else:
        level = "CRITICAL"
        color = "red"

    return {
        "score": score,
        "level": level,
        "color": color,
        "details": details
    }