import os
import requests
import whois
import time
import dns.resolver

from langchain.tools import tool

@tool
def get_subdomains(domain:str):
    """
    Obtiene una lista de subdominios de un dominio dado
    consultando los certificados SSL públicos en crt.sh.
    """

    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        headers = {"User-Agent": "Mozilla/5.0"}

        for intento in range(3):
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200 and response.text.strip():
                break
            time.sleep(2)
        
        datos = response.json()

        subdominios=[]
        for x in datos:
            subdominios.append(x["name_value"])

        # set() convierte la lista de subdominios en un conjunto
        # los conjuntos en Python no permiten duplicados, por lo que los elimina automáticamente
        # list convierte el conjunto de nuevo en una lista
        return list(set(subdominios))
    except Exception as e:
        return(f"Error al consultar crt.sh: {str(e)}")

@tool
def get_whois_info(domain:str):
    """
    Consulta una base de datos públicas de registro de dominios y devuelve
    información como quién registró el dominio y cuándo, fecha de expiración,
    servidores DNS que usa, datos de contacto del registrante, etc.
    """
    whois_data = {}

    try: 
        resultado = whois.whois(domain)

        whois_data = {
            "domain_name":resultado["domain_name"],
            "registrar":resultado["registrar"],
            "creation_date":resultado["creation_date"],
            "expiration_date":resultado["expiration_date"],
            "country":resultado["country"],
            "org":resultado["org"],
            "name_servers":resultado["name_servers"]
        }

    except Exception as e:
        print(f"Error al utilizar la herramienta whois: {str(e)}")

    return whois_data

@tool
def get_dns_records(domain:str):
    """
    Consulta los registros DNS de un dominio dado.
    Devuelve registros de tipo A (IPs), MX (servidores de correo),
    TXT (verificaciones y políticas de seguridad) y NS (servidores DNS).
    Útil para mapear la infraestructura y servicios del dominio.
    """

    records = {
        "A": [],
        "MX":[],
        "TXT":[],
        "NS":[]
    }

    try:
        for record in dns.resolver.resolve(domain, "A"):
            records["A"].append(str(record))
    except Exception as e:
        print(f"Error en A: {e}")
        pass

    try:
        for record in dns.resolver.resolve(domain, "MX"):
            records["MX"].append(str(record))
    except Exception as e:
        print(f"Error en MX: {e}")
        pass

    try:
        for record in dns.resolver.resolve(domain, "TXT"):
            records["TXT"].append(str(record))
    except Exception as e:
        print(f"Error en TXT: {e}")
        pass

    try:
        for record in dns.resolver.resolve(domain, "NS"):
            records["NS"].append(str(record))       
    except Exception as e:
        print(f"Error en NS: {e}")
        pass

    return records

@tool
def get_http_headers(domain: str):
    """
    Analiza las cabeceras HTTP de seguridad de un dominio.
    Detecta cabeceras de seguridad presentes y ausentes, y tecnologías expuestas.
    Útil para evaluar el nivel de seguridad web del objetivo.
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
        
        resultado = {
            "status_code": response.status_code,
            "server": response.headers.get("Server", "No expuesto"),
            "x_powered_by": response.headers.get("X-Powered-By", "No expuesto"),
            "security_headers_present": [],
            "security_headers_missing": []
        }
        
        for header in security_headers:
            if header in response.headers:
                resultado["security_headers_present"].append(header)
            else:
                resultado["security_headers_missing"].append(header)
        
        return resultado
    except Exception as e:
        return f"Error al analizar headers de {domain}: {str(e)}"

@tool
def check_hibp(domain: str):
    """
    Verifica si emails del dominio han aparecido en filtraciones de datos.
    Usa HaveIBeenPwned si hay API key configurada, o BreachDirectory como alternativa gratuita.
    Útil para evaluar el riesgo de exposición de credenciales del dominio.
    """
    try:
        hibp_api_key = os.getenv("HIBP_API_KEY")
        
        if hibp_api_key:
            # Usar HIBP con API key
            headers = {
                "hibp-api-key": hibp_api_key,
                "User-Agent": "osint-recon-agent"
            }
            url = f"https://haveibeenpwned.com/api/v3/breacheddomain/{domain}"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "fuente": "HaveIBeenPwned",
                    "domain": domain,
                    "emails_comprometidos": len(data),
                    "detalle": data
                }
            elif response.status_code == 404:
                return {"fuente": "HaveIBeenPwned", "domain": domain, "resultado": "Sin filtraciones encontradas"}
            else:
                return f"Error HIBP: status code {response.status_code}"
        
        else:
            # Usar LeakCheck como alternativa gratuita
            url = f"https://leakcheck.io/api/public?check={domain}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "fuente": "LeakCheck (alternativa gratuita)",
                    "domain": domain,
                    "resultado": data
                }
            else:
                return f"Error LeakCheck: status code {response.status_code}"
    
    except Exception as e:
        return f"Error al verificar filtraciones: {str(e)}"
