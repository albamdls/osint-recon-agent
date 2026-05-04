from pydantic import BaseModel, Field
from typing import Optional

class WhoisInfo(BaseModel):
    domain: str = ""
    registrar: str = ""
    creation_date: str = ""
    expiration_date: str = ""
    country: str = ""
    organization: str = ""
    name_servers: list[str] = []

class DNSInfo(BaseModel):
    a_records: list[str] = []
    mx_records: list[str] = []
    ns_records: list[str] = []
    txt_records: list[str] = []

class HeadersInfo(BaseModel):
    status_code: int = 0
    server: str = ""
    present_headers: list[str] = []
    missing_headers: list[str] = []

class BreachesInfo(BaseModel):
    source: str = ""
    total_records: int = 0
    exposed_fields: list[str] = []

class ReconReport(BaseModel):
    domain: str
    analysis_date: str = ""
    whois: Optional[WhoisInfo] = None
    dns: Optional[DNSInfo] = None
    subdomains: list[str] = []
    headers: Optional[HeadersInfo] = None
    breaches: Optional[BreachesInfo] = None
    risk_level: str = ""
    summary: str = ""
    recommendations: list[str] = []
    failed_tools: list[str] = []