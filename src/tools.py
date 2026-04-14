import requests
import whois

def get_subdomains(domain:str):
    
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

def get_whois_info(domain:str):
    whois_data = {}

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



if __name__ == "__main__":
    print(get_subdomains("github.com")[:3])
    print(get_whois_info("github.com"))