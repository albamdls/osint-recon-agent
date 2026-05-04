# Filtraciones de Datos y Credenciales Comprometidas

## Tipos de Filtraciones

### Stealer Logs
Credenciales capturadas por malware instalado en equipos de usuarios.
- Origen: troyanos, keyloggers, infostealers (Redline, Vidar, Raccoon)
- Datos típicos: usuario, contraseña, URL, cookies de sesión, IP
- Severidad: CRÍTICA — credenciales activas en el momento del robo
- Indicador OSINT: aparición en LeakCheck o HIBP como "Stealer Logs"

### Brechas de Bases de Datos
Volcados de bases de datos robadas de servicios comprometidos.
- Origen: ataques a servidores, inyecciones SQL, configuraciones erróneas
- Datos típicos: email, contraseña hasheada, datos de perfil
- Severidad: ALTA — depende de la antigüedad y tipo de hash
- Indicador OSINT: nombre del servicio comprometido y fecha

### Credential Stuffing Lists
Listas de credenciales compiladas de múltiples filtraciones.
- Origen: combinación de múltiples brechas anteriores
- Uso malicioso: ataques automatizados de relleno de credenciales
- Severidad: ALTA — si el usuario reutiliza contraseñas

### Phishing Kits
Credenciales capturadas mediante páginas falsas.
- Origen: campañas de phishing dirigidas
- Datos típicos: usuario, contraseña en texto plano, IP, fecha
- Severidad: CRÍTICA — contraseñas en texto plano

## Interpretación de Resultados HIBP/LeakCheck

### Por número de registros
- 0 registros: sin filtraciones detectadas — BAJO
- 1-10 registros: exposición mínima — BAJO/MEDIO
- 10-100 registros: exposición moderada — MEDIO
- 100-1000 registros: exposición significativa — ALTO
- +1000 registros: exposición crítica — CRÍTICO

### Por tipo de datos expuestos
- Solo email: severidad BAJA
- Email + contraseña hasheada: severidad MEDIA
- Email + contraseña en texto plano: severidad CRÍTICA
- Email + contraseña + datos personales: severidad CRÍTICA
- Cookies de sesión: severidad CRÍTICA (acceso inmediato)

### Por antigüedad
- Menos de 1 año: severidad ALTA (credenciales probablemente activas)
- 1-3 años: severidad MEDIA
- Más de 3 años: severidad BAJA (credenciales probablemente cambiadas)

## Recomendaciones según nivel de exposición

### Exposición BAJA
- Monitorear periódicamente nuevas filtraciones
- Verificar que las contraseñas expuestas no se reutilizan

### Exposición MEDIA
- Forzar cambio de contraseñas en el dominio afectado
- Implementar autenticación de dos factores (2FA)
- Notificar a usuarios afectados

### Exposición ALTA/CRÍTICA
- Reseteo inmediato de credenciales
- Investigar si hubo acceso no autorizado
- Activar monitoreo de seguridad intensivo
- Considerar notificación a autoridades (RGPD si aplica en Europa)
- Contratar auditoría de seguridad externa