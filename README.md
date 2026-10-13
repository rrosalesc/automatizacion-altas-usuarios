# Automatización de Altas de Usuario

Bot en Python que automatiza el proceso de alta de nuevos usuarios,
integrando un **sistema de tickets** (tipo Jira), un **directorio
corporativo** (tipo Active Directory) y un **sistema de gestión de
activos/inventario** (tipo Snipe-IT) a través de sus APIs.

> **Nota sobre este repositorio:** es una versión de referencia
> reconstruida a partir de una automatización que desarrollé en mis
> prácticas profesionales para agilizar el alta de usuarios por piso.
> El código original es propiedad de la empresa y no se publica. Aquí
> uso nombres y datos genéricos, y el flujo se puede ver funcionando
> con datos ficticios mediante el modo demo (ver abajo).

## Problema que resuelve

El alta manual de un nuevo usuario requería revisar tickets uno por
uno, crear el usuario en el directorio corporativo, registrarlo en el
sistema de inventario, y documentar manualmente cada paso — un proceso
repetitivo y propenso a errores humanos. Este bot automatiza todo ese
flujo.

## Flujo del proceso

1. Se ejecuta manualmente desde terminal (VS Code) para revisar los
   tickets pendientes.
2. **Detecta** tickets nuevos de "alta de usuario" en el sistema de
   tickets, con los datos del nuevo empleado: nombre, puesto,
   departamento y jefe directo, filtrando por piso/ubicación.
3. **Crea el usuario** en el directorio corporativo con esos datos,
   dejándolo listo y pendiente de que un administrador le asigne la
   licencia de Microsoft 365.
4. **Registra el usuario** en el sistema de gestión de activos
   (reutilizando el username ya generado en el directorio), para
   poder asignarle equipo (laptop, monitor, etc.) después.
5. **Documenta la acción** dejando un comentario automático en el
   ticket original, detallando qué se hizo y qué queda pendiente
   (la asignación manual de la licencia).
6. Si un ticket falla, el error se registra y el proceso **continúa**
   con los demás tickets (un error no detiene todo el flujo).

## Probarlo en 10 segundos (modo demo)

El modo demo corre el flujo completo con tickets ficticios, sin
credenciales y sin instalar nada (solo necesita Python 3):

```bash
python src/main.py --demo
```

Qué vas a ver: dos tickets procesados de principio a fin (usuario creado
en el directorio, registrado en el inventario y comentario final en el
ticket con la licencia pendiente) y un tercer ticket con el puesto vacío
que falla a propósito, para mostrar que el error se registra y el bot
continúa con los demás.

## Estado del proyecto

- **Modo demo:** probado y funcionando.
- **Modo real:** los clientes de `src/` usan URLs y campos genéricos y
  **no se han probado contra un Jira, Snipe-IT o Active Directory
  reales**. Para usarlo en un entorno propio hay que adaptar los
  endpoints y los nombres de los campos a cada sistema.

## Tecnologías usadas

- **Python 3** — lógica principal del bot
- **Requests** — consumo de APIs REST
- **python-dotenv** — manejo seguro de credenciales por variables de entorno
- **logging** — registro de eventos y errores

## Estructura del proyecto

```
automatizacion-altas-usuarios/
├── src/
│   ├── main.py                    # Orquestador principal del flujo
│   ├── demo_clients.py            # Clientes simulados con datos ficticios
│   ├── ticketing_client.py        # Cliente API del sistema de tickets
│   ├── asset_management_client.py # Cliente API del sistema de inventario
│   ├── directory_client.py        # Cliente API del directorio corporativo
│   └── config.py                  # Carga de configuración/credenciales
├── .env.example                   # Plantilla de variables de entorno
├── requirements.txt
└── README.md
```

## Cómo correrlo con sistemas reales

```bash
# 1. Clona el repositorio
git clone <url-del-repo>
cd automatizacion-altas-usuarios

# 2. Instala dependencias
pip install -r requirements.txt

# 3. Configura tus credenciales
cp .env.example .env
# edita .env con tus propios valores

# 4. Ejecuta el bot
python src/main.py
```

## Qué aprendí / apliqué en este proyecto

- Consumo e integración de múltiples APIs REST en un solo flujo.
- Manejo de credenciales de forma segura (variables de entorno, nunca
  hardcodeadas en el código).
- Manejo de errores por elemento individual, para que una falla no
  detenga todo el proceso.
- Logging estructurado para dar seguimiento y trazabilidad a lo que
  hace el bot.
- División del código en módulos claros, cada uno con una sola
  responsabilidad.
- Separación entre la lógica del flujo y los clientes de cada sistema,
  lo que permite cambiar los clientes reales por simulados (modo demo)
  sin modificar el flujo.

## Autor

**Rigoberto Rosales Cervantes** — Estudiante de Ingeniería en
Tecnologías Computacionales | [LinkedIn](https://www.linkedin.com/in/rigoberto-cervantes-5b44b3282/)
