"""
Este modulo contiene todas las configuraciones de la aplicacion
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuraciones de la aplicacion

    Attributes:
        host (str): Nombre de host donde correra el agente
        port (int): Puerto donde correra el agente
        model (str): Nombre del model que se ejecutara en Ollama
    """

    # Configuración del agente comediante
    host: str = Field(
        default="localhost",
        description="Nombre de host donde correra el agente",
    )
    port: int = Field(
        default=8000,
        description="Port to run the agent on",
    )

    # Ollama settings
    model: str = Field(
        default="gemma3:4b",
        description="Model name that Ollama will execute",
    )


settings = Settings()
