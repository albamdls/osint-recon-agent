# Registros DNS y su Significado en OSINT

## Registro A
Mapea un dominio a una dirección IPv4.
- Uso OSINT: identificar el servidor físico o CDN que aloja el dominio
- Indicadores: IP en rango de Cloudflare (104.x.x.x) indica CDN protector
- Indicadores: IP directa del servidor puede revelar proveedor de hosting
- Riesgo: IP expuesta directamente puede ser objetivo de ataques DDoS

## Registro AAAA
Mapea un dominio a una dirección IPv6.
- Uso OSINT: mismo uso que registro A pero para IPv6
- Presencia indica infraestructura moderna con soporte dual-stack

## Registro MX
Indica los servidores de correo del dominio.
- Uso OSINT: identificar proveedor de email corporativo
- google.com en MX: usa Google Workspace
- outlook.com en MX: usa Microsoft 365
- Riesgo: revela servicios SaaS utilizados por la organización

## Registro TXT
Texto libre usado para verificaciones y políticas.
- SPF (v=spf1): política de envío de correo, previene spoofing
- DKIM: firma criptográfica de emails
- DMARC: política de autenticación de correo
- Verificaciones de terceros: revelan servicios SaaS integrados
- Uso OSINT: mapa completo de servicios usados por la organización

## Registro NS
Servidores DNS autoritativos del dominio.
- Uso OSINT: identificar proveedor DNS
- AWS Route 53: infraestructura en Amazon
- Cloudflare: protección DDoS y CDN
- NS propios: infraestructura DNS gestionada internamente

## Registro CNAME
Alias que apunta a otro dominio.
- Uso OSINT: revelar servicios de terceros (CDN, SaaS)
- Riesgo: Subdomain Takeover si el servicio apuntado se cancela

## Registro SOA
Información administrativa del dominio.
- Contiene: servidor primario, email del administrador, TTL
- Uso OSINT: email del administrador puede usarse en OSINT

## Indicadores de Riesgo en DNS
- Sin SPF configurado: riesgo de spoofing de correo — ALTO
- Sin DMARC: política de correo incompleta — MEDIO
- CNAME a servicios cancelados: riesgo de Subdomain Takeover — CRÍTICO
- NS únicos sin redundancia: riesgo de disponibilidad — MEDIO
- TTL muy bajo: posible uso de GeoDNS o cambios frecuentes — INFO