"""
ticketing_client.py

Cliente para interactuar con un sistema de tickets tipo Jira.
Se encarga de:
  - Buscar tickets nuevos de "alta de usuario" (ej. por piso/ubicación).
  - Dejar comentarios automáticos documentando lo que hizo el bot.

Nota: este es un ejemplo genérico para portafolio. En un entorno real,
la URL base y el token se cargan desde variables de entorno (.env),
nunca se escriben directo en el código.
"""

import requests
from config import TICKETING_BASE_URL, TICKETING_API_TOKEN


HEADERS = {
    "Authorization": f"Bearer {TICKETING_API_TOKEN}",
    "Content-Type": "application/json",
}


def get_pending_new_hire_tickets(floor: str = None) -> list[dict]:
    """
    Busca tickets abiertos de tipo 'Alta de usuario'.

    Args:
        floor: si se especifica, filtra solo tickets de ese piso/ubicación.

    Returns:
        Lista de tickets, cada uno como diccionario con al menos:
        {id, nombre_usuario, puesto, departamento, jefe, piso, estado}
    """
    params = {"status": "open", "type": "alta_usuario"}
    if floor:
        params["floor"] = floor

    response = requests.get(
        f"{TICKETING_BASE_URL}/tickets",
        headers=HEADERS,
        params=params,
        timeout=10,
    )
    response.raise_for_status()
    return response.json().get("tickets", [])


def post_comment(ticket_id: str, message: str) -> None:
    """
    Deja un comentario automático en un ticket, documentando la acción
    que realizó el bot (ej. "Usuario creado en Active Directory").

    Args:
        ticket_id: identificador del ticket.
        message: texto del comentario.
    """
    response = requests.post(
        f"{TICKETING_BASE_URL}/tickets/{ticket_id}/comments",
        headers=HEADERS,
        json={"body": message},
        timeout=10,
    )
    response.raise_for_status()
