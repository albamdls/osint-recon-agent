# Cabeceras de Seguridad HTTP

## Strict-Transport-Security (HSTS)
Fuerza al navegador a usar HTTPS en lugar de HTTP.
- Ausencia: riesgo de ataques de downgrade y MITM
- Presencia: protección contra interceptación de tráfico
- Severidad si ausente: MEDIA

## Content-Security-Policy (CSP)
Define qué recursos puede cargar el navegador.
- Ausencia: vulnerabilidad a ataques XSS e inyección de contenido
- Presencia: previene ejecución de scripts maliciosos
- Severidad si ausente: ALTA

## X-Frame-Options
Previene que la página sea embebida en iframes.
- Ausencia: vulnerable a ataques de clickjacking
- Presencia: protección contra clickjacking
- Severidad si ausente: MEDIA

## X-Content-Type-Options
Evita que el navegador interprete ficheros con tipo MIME incorrecto.
- Ausencia: vulnerable a MIME sniffing
- Presencia: previene ejecución de contenido malicioso
- Severidad si ausente: BAJA

## Referrer-Policy
Controla qué información de referencia se envía al navegar.
- Ausencia: posible fuga de URLs internas
- Presencia: protección de privacidad y datos internos
- Severidad si ausente: BAJA

## Permissions-Policy
Controla qué APIs del navegador puede usar la página.
- Ausencia: acceso no restringido a cámara, micrófono, geolocalización
- Presencia: principio de mínimo privilegio en APIs
- Severidad si ausente: BAJA

## Puntuación de Seguridad HTTP
- 6/6 cabeceras presentes: EXCELENTE
- 5/6 cabeceras presentes: MUY BUENO
- 4/6 cabeceras presentes: BUENO
- 3/6 cabeceras presentes: MEDIO
- 2/6 o menos: DEFICIENTE