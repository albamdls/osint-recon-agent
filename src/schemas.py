from pydantic import BaseModel, Field
from typing import Optional

class WhoisInfo(BaseModel):
    dominio: str = ""
    registrador: str = ""
    fecha_creacion: str = ""
    fecha_expiracion: str = ""
    pais: str = ""
    organizacion: str = ""
    servidores_dns: list[str] = []

class DNSInfo(BaseModel):
    registros_a: list[str] = []
    registros_mx: list[str] = []
    registros_ns: list[str] = []
    registros_txt: list[str] = []

class HeadersInfo(BaseModel):
    status_code: int = 0
    servidor: str = ""
    cabeceras_presentes: list[str] = []
    cabeceras_ausentes: list[str] = []

class FiltracionesInfo(BaseModel):
    fuente: str = ""
    total_registros: int = 0
    campos_expuestos: list[str] = []

class ReconReport(BaseModel):
    dominio: str
    fecha_analisis: str = ""
    whois: Optional[WhoisInfo] = None
    dns: Optional[DNSInfo] = None
    subdominios: list[str] = []
    headers: Optional[HeadersInfo] = None
    filtraciones: Optional[FiltracionesInfo] = None
    nivel_riesgo: str = ""
    resumen: str = ""
    recomendaciones: list[str] = []
    herramientas_fallidas: list[str] = []