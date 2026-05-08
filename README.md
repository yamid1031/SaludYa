# SaludYa

Aplicación web sencilla para gestionar acceso de pacientes, registro de usuarios y agendamiento de citas médicas. Está construida con Flask, Jinja2 y SQLite, y funciona completamente en local.

## Funcionalidades

- Inicio de sesión con correo y contraseña.
- Registro de nuevos usuarios.
- Panel principal con accesos rápidos.
- Agendamiento de citas por fecha, hora y servicio.
- Historial de citas por usuario autenticado.
- Mensajes visuales de éxito y error.
- Interfaz responsiva para escritorio y móvil.

## Especialidades disponibles en agendamiento

- Consulta general
- Medicina interna
- Odontología
- Pediatría
- Ginecología
- Otorrinolaringología
- Dermatología
- Cardiología

## Tecnologías

- Python 3.14.3
- Flask 3.1.3
- Jinja2
- SQLite
- CSS propio

## Estructura principal

```text
SaludYa/
├── app.py
├── requirements.txt
├── saludya.db
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── login.html
    ├── registro.html
    ├── panel.html
    ├── cita.html
    └── historial.html
```

## Usuarios actuales en la base local

La base `saludya.db` tiene estos accesos cargados actualmente:

- `yamidthyme@gmail.com` / `Yazeib31`
- `yezidcasimiro@gmail.com` / `Yazeib31`

Observación:

- El correo `yezidcasimiro@gmail.com` aparece duplicado en la base.
- Las contraseñas se guardan en texto plano en esta versión del proyecto.

## Cómo instalar y correr en local

### 1. Entrar a la carpeta del proyecto

```powershell
cd D:\usuario\Downloads\SaludYa\SaludYa
```

### 2. Crear entorno virtual

```powershell
python -m venv .venv
```

### 3. Activar entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación, ejecuta primero:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\.venv\Scripts\Activate.ps1
```

### 4. Instalar dependencias

```powershell
python -m pip install -r requirements.txt
```

### 5. Iniciar la aplicación

```powershell
python app.py
```

### 6. Abrir la aplicación

En el navegador:

```text
http://127.0.0.1:5000
```

## Cómo funciona internamente

### Rutas principales

- `/` muestra el login.
- `/registro` muestra el formulario de registro.
- `/guardar` crea un usuario nuevo.
- `/ingresar` valida credenciales y crea la sesión.
- `/panel` muestra el panel principal del usuario autenticado.
- `/cita` muestra el formulario de agendamiento.
- `/guardar_cita` guarda una nueva cita.
- `/historial` muestra las citas del usuario autenticado.
- `/logout` cierra la sesión.

### Base de datos

El archivo local de datos es `saludya.db`.

Tablas usadas:

- `usuarios`
  - `id`
  - `nombre`
  - `correo`
  - `contraseña`
- `citas`
  - `id`
  - `correo`
  - `fecha`
  - `hora`
  - `servicio`

## Diseño actual

- Login y registro simplificados con espacio visual listo para reemplazar por el logo oficial de SaludYa.
- Navegación superior para usuarios autenticados.
- Pantalla de cita con acción principal única para agendar.
- Historial con tabla para escritorio y tarjetas legibles en móvil.

## Limitaciones actuales

- No hay cifrado de contraseñas.
- No hay validación de correos duplicados.
- No hay roles de usuario.
- No hay cancelación ni edición de citas.
- No hay validación de disponibilidad por hora o especialidad.

## Recomendaciones siguientes

- Cifrar contraseñas con `werkzeug.security`.
- Evitar registros duplicados por correo.
- Permitir editar o cancelar citas.
- Agregar más datos a cada cita, como profesional, sede o estado.
- Reemplazar el espacio de logo por el icono oficial en `templates/login.html`, `templates/registro.html` y `templates/base.html`.
