"""
directory_client.py

Cliente para crear usuarios en un servicio de directorio tipo Active
Directory. El usuario se crea deshabilitado para licencia (pendiente),
listo para que un administrador asigne la licencia correspondiente.

Nota: en un entorno real esto normalmente se hace con una librería como
`ldap3` conectándose directo al controlador de dominio. Aquí se modela
como una llamada HTTP genérica para mantener el ejemplo simple y
portable (sin depender de infraestructura de red real).
"""

import requests
from config import DIRECTORY_BASE_URL, DIRECTORY_API_TOKEN


HEADERS = {
    "Authorization": f"Bearer {DIRECTORY_API_TOKEN}",
    "Content-Type": "application/json",
}


def create_directory_user(
    full_name: str,
    job_title: str,
    department: str,
    manager: str,
    floor: str,
    employee_id: str,
) -> dict:
    """
    Crea un usuario nuevo en el directorio corporativo, con los datos
    obtenidos del ticket (puesto, departamento, jefe directo), listo
    para que se le asigne una licencia de Microsoft 365 manualmente.

    Args:
        full_name: nombre completo del usuario.
        job_title: puesto del usuario.
        department: departamento al que pertenece.
        manager: nombre del jefe directo.
        floor: piso/ubicación (se usa para la unidad organizativa).
        employee_id: identificador único del empleado.

    Returns:
        Diccionario con el usuario creado (incluye username generado).
    """
    username = _generate_username(full_name, employee_id)

    payload = {
        "username": username,
        "full_name": full_name,
        "job_title": job_title,
        "department": department,
        "manager": manager,
        "organizational_unit": f"OU=Piso-{floor}",
        "license_assigned": False,  # licencia M365 queda pendiente para el admin
    }

    response = requests.post(
        f"{DIRECTORY_BASE_URL}/users",
        headers=HEADERS,
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def _generate_username(full_name: str, employee_id: str) -> str:
    """Genera un nombre de usuario simple a partir del nombre y el ID."""
    first_name = full_name.split()[0].lower()
    return f"{first_name}.{employee_id}"
