# OWASP Top 10 — Vulnerabilidades Web más Críticas

## A01 - Control de Acceso Roto
Restricciones de acceso no implementadas correctamente.
- Síntomas: acceso a recursos sin autenticación, escalada de privilegios
- Impacto: CRÍTICO
- Detección OSINT: endpoints expuestos, paneles admin accesibles

## A02 - Fallos Criptográficos
Datos sensibles expuestos por falta de cifrado o cifrado débil.
- Síntomas: HTTP en lugar de HTTPS, algoritmos débiles, datos en texto plano
- Impacto: ALTO
- Detección OSINT: ausencia de HSTS, certificados caducados

## A03 - Inyección
Datos no validados enviados a intérpretes (SQL, NoSQL, OS, LDAP).
- Síntomas: inputs sin sanitizar, mensajes de error con detalles técnicos
- Impacto: CRÍTICO
- Detección OSINT: tecnologías expuestas en headers (X-Powered-By)

## A04 - Diseño Inseguro
Falta de controles de seguridad en el diseño de la aplicación.
- Síntomas: ausencia de rate limiting, flujos de negocio sin validar
- Impacto: ALTO

## A05 - Configuración de Seguridad Incorrecta
Configuraciones por defecto, incompletas o erróneas.
- Síntomas: cabeceras de seguridad ausentes, servicios innecesarios expuestos
- Impacto: ALTO
- Detección OSINT: cabeceras HTTP ausentes, puertos abiertos innecesarios

## A06 - Componentes Vulnerables y Desactualizados
Uso de librerías y frameworks con vulnerabilidades conocidas.
- Síntomas: versiones antiguas expuestas en headers o metadatos
- Impacto: ALTO
- Detección OSINT: versiones de software en Server header, X-Powered-By

## A07 - Fallos de Identificación y Autenticación
Implementación incorrecta de autenticación y gestión de sesiones.
- Síntomas: contraseñas débiles, sesiones sin expiración, credenciales expuestas
- Impacto: ALTO
- Detección OSINT: credenciales en filtraciones (HIBP), subdominios de login

## A08 - Fallos de Integridad de Software y Datos
Código y datos sin verificación de integridad.
- Síntomas: pipelines CI/CD inseguros, dependencias sin verificar
- Impacto: ALTO

## A09 - Fallos en Registro y Monitoreo
Ausencia de logging adecuado que permita detectar ataques.
- Síntomas: sin alertas de seguridad, logs insuficientes
- Impacto: MEDIO

## A10 - Falsificación de Solicitudes del Lado del Servidor (SSRF)
El servidor realiza peticiones a recursos internos no autorizados.
- Síntomas: parámetros URL que aceptan direcciones internas
- Impacto: CRÍTICO
- Detección OSINT: endpoints que aceptan URLs como parámetro