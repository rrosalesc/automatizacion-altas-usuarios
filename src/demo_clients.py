"""
demo_clients.py

Versiones simuladas de los tres clientes (tickets, directorio e inventario)
para poder correr el flujo completo SIN credenciales ni sistemas reales.

Los datos son ficticios. Cada función tiene la misma firma que su
contraparte real, así que main.py no necesita saber si está en modo
demo o en modo real.
"""

# Tickets de ejemplo, como los devolvería el sistema de tickets.
# El tercero tiene un campo faltante a propósito, para mostrar cómo el
# bot registra el error y continúa con los demás.
_FAKE_TICKETS = [
    {
        "id": "ALTA-101",
        "nombre_usuario": "Ana Torres",
        "puesto": "Analista de Finanzas",
        "departamento": "Finanzas",
        "jefe": "Luis Herrera",
        "piso": "5",
        "estado": "open",
    },
    {
        "id": "ALTA-102",
        "nombre_usuario": "Carlos Mendoza",
        "puesto": "Desarrollador",
        "departamento": "Tecnología",
        "jefe": "Marta Ríos",
        "piso": "20",
        "estado": "open",
    },
    {
        "id": "ALTA-103",
        "nombre_usuario": "Sofía Pérez",
        # Falta "puesto": simula un ticket mal llenado
        "departamento": "Recursos Humanos",
        "jefe": "Jorge Salas",
        "piso": "5",
        "estado": "open",
    },
]


def get_pending_new_hire_tickets(floor: str = None) -> list[dict]:
    """Devuelve los tickets de ejemplo, filtrados por piso."""
    return [t for t in _FAKE_TICKETS if floor is None or t["piso"] == floor]


def post_comment(ticket_id: str, message: str) -> None:
    """En vez de llamar a la API, muestra el comentario en pantalla."""
    print(f"   [DEMO] Comentario en ticket {ticket_id}:")
    for line in message.splitlines():
        print(f"          {line}")


def create_directory_user(
    full_name: str,
    job_title: str,
    department: str,
    manager: str,
    floor: str,
    employee_id: str,
) -> dict:
    """Simula la creación del usuario en el directorio."""
    first_name = full_name.split()[0].lower()
    username = f"{first_name}.{employee_id}".lower()
    print(f"   [DEMO] Directorio: usuario '{username}' creado en OU=Piso-{floor}")
    return {"username": username}


def create_user_record(
    full_name: str,
    job_title: str,
    department: str,
    username: str,
    floor: str,
    employee_id: str,
) -> dict:
    """Simula el registro del usuario en el sistema de inventario."""
    print(f"   [DEMO] Inventario: usuario '{username}' registrado ({department})")
    return {"id": employee_id}
