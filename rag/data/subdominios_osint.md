# Subdominios y Reconocimiento OSINT

## Importancia de los Subdominios en OSINT

Los subdominios revelan la arquitectura interna de una organización,
servicios utilizados, entornos de desarrollo y posibles vectores de ataque.

## Categorías de Subdominios por Riesgo

### Subdominios de Alta Sensibilidad — Riesgo ALTO
- admin.*, panel.*, cpanel.*: paneles de administración
- vpn.*, remote.*, rdp.*: acceso remoto corporativo
- staging.*, dev.*, test.*, uat.*: entornos de desarrollo
- api.*, api-internal.*: APIs potencialmente sin autenticación
- mail.*, webmail.*, smtp.*: servicios de correo
- jenkins.*, gitlab.*, git.*: herramientas de desarrollo
- jira.*, confluence.*: gestión de proyectos interna

### Subdominios de Sensibilidad Media — Riesgo MEDIO
- blog.*, news.*: posibles CMS desactualizados
- shop.*, store.*: plataformas de comercio electrónico
- cdn.*, static.*: servidores de contenido estático
- support.*, help.*: plataformas de soporte
- login.*, auth.*, sso.*: sistemas de autenticación

### Subdominios Informativos — Riesgo BAJO
- www.*: sitio web principal
- docs.*, documentation.*: documentación pública
- status.*: página de estado de servicios
- careers.*, jobs.*: recursos humanos

## Técnicas de Descubrimiento de Subdominios

### Certificate Transparency (crt.sh)
Registros públicos de certificados SSL/TLS emitidos.
- Ventaja: registros históricos, muy completo
- Limitación: solo dominios con certificados SSL
- Uso: detectar subdominios olvidados con certificados caducados

### DNS Brute Force
Prueba de subdominios comunes mediante diccionario.
- Ventaja: descubre subdominios sin certificado SSL
- Limitación: no descubre subdominios no estándar

### Registros DNS pasivos
Histórico de resoluciones DNS almacenadas por terceros.
- Herramientas: SecurityTrails, PassiveTotal, Shodan

## Indicadores de Riesgo en Subdominios

### Subdomain Takeover
Subdominio apunta a servicio externo cancelado.
- Detección: CNAME a servicio que devuelve 404 o "not found"
- Severidad: CRÍTICA — permite tomar control del subdominio
- Servicios comunes afectados: GitHub Pages, Heroku, AWS S3

### Entornos de Desarrollo Expuestos
- staging.*, dev.* accesibles públicamente
- Severidad: ALTA — suelen tener menos controles de seguridad
- Riesgo: datos de prueba, credenciales hardcodeadas

### Wildcards DNS
Registro *.dominio.com que resuelve cualquier subdominio.
- Uso legítimo: CDNs, servicios multi-tenant
- Riesgo: dificulta detección de subdominios reales

## Patrones de Infraestructura por Subdominios

### Empresas que usan Google Workspace
- mail.dominio.com → Google
- MX: aspmx.l.google.com

### Empresas que usan Microsoft 365
- MX: *.mail.protection.outlook.com
- autodiscover.dominio.com

### Empresas con infraestructura en AWS
- NS: awsdns-*.com
- s3.dominio.com, assets.dominio.com → S3

### Empresas protegidas por Cloudflare
- NS: *.ns.cloudflare.com
- IP en rango 104.x.x.x o 172.64.x.x