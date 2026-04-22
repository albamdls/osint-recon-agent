import requests
import whois

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
        response = requests.get(url, headers=headers)
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

        return whois_data
    except Exception as e:
        print(f"Error al utilizar la herramienta whois: {str(e)}")