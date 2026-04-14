import requests

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

if __name__ == "__main__":
    resultado = get_subdomains("github.com")
    print(resultado[:3])    