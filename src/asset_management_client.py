"""
asset_management_client.py

Cliente para interactuar con un sistema de gestión de activos/inventario
tipo Snipe-IT. Se encarga de registrar al nuevo usuario como "asset owner"
dentro del inventario de la empresa.

Nota: ejemplo genérico para portafolio, sin credenciales ni URLs reales.
"""

import requests
from config import ASSET_SYSTEM_BASE_URL, ASSET_SYSTEM_API_TOKEN


HEADERS = {
    "Authorization": f"Bearer {ASSET_SYSTEM_API_TOKEN}",
    "Content-Type": "application/json",
}


def create_user_record(
    full_name: str,
    job_title: str,
    department: str,
    username: str,
    floor: str,
    employee_id: str,
) -> dict:
    """
    Crea el registro de un nuevo usuario dentro del sistema de inventario,
    reutilizando los datos ya creados en el directorio corporativo
    (incluyendo el username generado ahí), para poder asignarle equipo
    (laptop, monitor, etc.) más adelante.

    Args:
        full_name: nombre completo del usuario.
        job_title: puesto del usuario.
        department: departamento al que pertenece.
        username: nombre de usuario ya creado en el directorio.
        floor: piso/ubicación donde trabajará.
        employee_id: identificador único del empleado.

    Returns:
        Diccionario con la respuesta del sistema (incluye el id creado).
    """
    payload = {
        "name": full_name,
        "job_title": job_title,
        "department": department,
        "username": username,
        "location": floor,
        "employee_num": employee_id,
    }

    response = requests.post(
        f"{ASSET_SYSTEM_BASE_URL}/users",
        headers=HEADERS,
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()
