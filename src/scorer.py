from src.schemas import ReconReport

def calcular_score(reporte: ReconReport) -> dict:
    """
    Calcula un score de riesgo basado en los hallazgos del informe.
    Devuelve score numérico y nivel de riesgo.
    """
    score = 0
    detalles = []

    # WHOIS
    if reporte.whois:
        if reporte.whois.registrador:
            score -= 5
            detalles.append(("✅ Registrador profesional", -5))

    # Headers HTTP
    if reporte.headers:
        cabeceras_criticas = {
            "Content-Security-Policy": 25,
            "Strict-Transport-Security": 20,
            "X-Frame-Options": 15,
            "X-Content-Type-Options": 10,
            "Referrer-Policy": 5,
            "Permissions-Policy": 5
        }
        for cabecera, puntos in cabeceras_criticas.items():
            if cabecera in reporte.headers.cabeceras_ausentes:
                score += puntos
                detalles.append((f"❌ {cabecera} ausente", +puntos))
            else:
                score -= round(puntos * 0.3)
                detalles.append((f"✅ {cabecera} presente", -round(puntos * 0.3)))

    # Filtraciones
    if reporte.filtraciones:
        total = reporte.filtraciones.total_registros
        if total == 0:
            score -= 10
            detalles.append(("✅ Sin filtraciones detectadas", -10))
        elif total < 10:
            score += 10
            detalles.append((f"⚠️ {total} filtraciones", +10))
        elif total < 100:
            score += 20
            detalles.append((f"⚠️ {total} filtraciones", +20))
        elif total < 1000:
            score += 35
            detalles.append((f"🚨 {total} filtraciones", +35))
        else:
            score += 50
            detalles.append((f"🚨 +1000 filtraciones", +50))

    # Subdominios sensibles
    subdominios_riesgo = ["admin", "staging", "dev", "test", "vpn", "jenkins", "jira"]
    if reporte.subdominios:
        encontrados = [s for s in reporte.subdominios 
                      if any(r in s.lower() for r in subdominios_riesgo)]
        if encontrados: 
            score += len(encontrados) * 5
            detalles.append((f"⚠️ {len(encontrados)} subdominios sensibles", +len(encontrados)*5))

    # Herramientas fallidas
    if reporte.herramientas_fallidas:
        score += len(reporte.herramientas_fallidas) * 3
        detalles.append((f"⚠️ {len(reporte.herramientas_fallidas)} herramientas fallidas", 
                         +len(reporte.herramientas_fallidas)*3))

    # Calcular nivel
    if score <= 10:
        nivel = "BAJO"
        color = "green"
    elif score <= 30:
        nivel = "MEDIO"
        color = "yellow"
    elif score <= 60:
        nivel = "ALTO"
        color = "orange"
    else:
        nivel = "CRÍTICO"
        color = "red"

    return {
        "score": score,
        "nivel": nivel,
        "color": color,
        "detalles": detalles
    }