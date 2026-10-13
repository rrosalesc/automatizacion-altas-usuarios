"""
config.py

Carga la configuración (URLs y tokens) desde variables de entorno.
Nunca se deben escribir credenciales reales directamente en el código.

Para correr el proyecto localmente, copia `.env.example` a `.env`
y llena tus propios valores (o los de un entorno de pruebas).
"""

import os
from dotenv import load_dotenv

load_dotenv()

TICKETING_BASE_URL = os.getenv("TICKETING_BASE_URL", "")
TICKETING_API_TOKEN = os.getenv("TICKETING_API_TOKEN", "")

ASSET_SYSTEM_BASE_URL = os.getenv("ASSET_SYSTEM_BASE_URL", "")
ASSET_SYSTEM_API_TOKEN = os.getenv("ASSET_SYSTEM_API_TOKEN", "")

DIRECTORY_BASE_URL = os.getenv("DIRECTORY_BASE_URL", "")
DIRECTORY_API_TOKEN = os.getenv("DIRECTORY_API_TOKEN", "")
