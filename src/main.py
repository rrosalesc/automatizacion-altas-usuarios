"""
main.py

Automatización de altas de usuario (proyecto de portafolio).

Flujo completo:
  1. Busca tickets nuevos de "alta de usuario" en el sistema de tickets,
     filtrando por piso.
  2. Por cada ticket encontrado:
     a. Crea el usuario en el directorio corporativo (queda listo,
        pendiente de asignar licencia).
     b. Registra al usuario en el sistema de gestión de activos.
     c. Deja un comentario automático en el ticket documentando lo
        que se hizo.
  3. Si algo falla en un ticket, se registra el error y se continúa
     con los demás (un ticket con problemas no debe detener todo el
     proceso).

Modos de ejecución:
  python src/main.py --demo   -> usa datos ficticios, sin credenciales
  python src/main.py          -> usa los clientes reales (requiere .env)

Versión de referencia reconstruida a partir de una automatización que
desarrollé en mis prácticas. El código original es propiedad de la
empresa y no se publica.
"""

import argparse
import logging
from collections import namedtuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Pisos que el bot revisa en cada corrida
MONITORED_FLOORS = ["5", "20"]

# Agrupa las cuatro funciones que el flujo necesita, para poder
# intercambiar los clientes reales por los de demo sin tocar la lógica.
Clients = namedtuple(
    "Clients",
    ["get_tickets", "post_comment", "create_directory_user", "create_user_record"],
)


def load_clients(demo: bool) -> Clients:
    """Carga los clientes reales o los simulados, según el modo."""
    if demo:
        import demo_clients as c
    else:
        # Estos imports leen la configuración (.env), por eso solo se
        # hacen en modo real: el demo corre sin dependencias externas.
        import ticketing_client as t
        import asset_management_client as a
        import directory_client as d

        return Clients(
            get_tickets=t.get_pending_new_hire_tickets,
            post_comment=t.post_comment,
            create_directory_user=d.create_directory_user,
            create_user_record=a.create_user_record,
        )

    return Clients(
        get_tickets=c.get_pending_new_hire_tickets,
        post_comment=c.post_comment,
        create_directory_user=c.create_directory_user,
        create_user_record=c.create_user_record,
    )


def process_ticket(ticket: dict, clients: Clients) -> None:
    """Procesa un solo ticket de alta de usuario, de principio a fin."""
    ticket_id = ticket["id"]
    full_name = ticket["nombre_usuario"]
    job_title = ticket["puesto"]
    department = ticket["departamento"]
    manager = ticket["jefe"]
    floor = ticket["piso"]
    employee_id = ticket["id"]  # simplificado para el ejemplo

    logger.info("Procesando alta de %s (piso %s)", full_name, floor)

    # 1. Crear usuario en el directorio (Active Directory), con los
    #    datos obtenidos del ticket de Jira (puesto, depto, jefe)
    directory_user = clients.create_directory_user(
        full_name, job_title, department, manager, floor, employee_id
    )
    logger.info("Usuario creado en directorio: %s", directory_user["username"])

    # 2. Registrar en el sistema de gestión de activos (Snipe-IT),
    #    reutilizando el username ya generado en el directorio
    clients.create_user_record(
        full_name,
        job_title,
        department,
        directory_user["username"],
        floor,
        employee_id,
    )
    logger.info("Usuario registrado en sistema de inventario")

    # 3. Documentar la acción en el ticket original, dejando claro
    #    qué queda pendiente (la licencia de Microsoft 365)
    comment = (
        f"Alta automática procesada por el bot:\n"
        f"- Usuario creado en Active Directory: {directory_user['username']} "
        f"(puesto: {job_title}, depto: {department}, jefe: {manager})\n"
        f"- Usuario registrado en sistema de inventario (piso {floor})\n"
        f"- Pendiente: asignación manual de licencia de Microsoft 365"
    )
    clients.post_comment(ticket_id, comment)
    logger.info("Comentario publicado en ticket %s", ticket_id)


def run(demo: bool = False) -> None:
    """Punto de entrada: revisa todos los pisos monitoreados y procesa altas."""
    clients = load_clients(demo)

    if demo:
        logger.info("Modo DEMO: datos ficticios, no se conecta a ningún sistema")

    for floor in MONITORED_FLOORS:
        tickets = clients.get_tickets(floor=floor)
        logger.info("Piso %s: %d tickets pendientes", floor, len(tickets))

        for ticket in tickets:
            try:
                process_ticket(ticket, clients)
            except Exception as exc:
                # Un ticket con error no debe detener el resto del proceso
                logger.error(
                    "Error procesando ticket %s: %s", ticket.get("id"), repr(exc)
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automatización de altas de usuario")
    parser.add_argument(
        "--demo",
        action="store_true",
        help="corre el flujo con datos ficticios, sin credenciales",
    )
    args = parser.parse_args()
    run(demo=args.demo)
