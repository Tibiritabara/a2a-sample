from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Configuración del agente comediante
    host: str = Field(
        default="localhost",
        description="Host to run the agent on",
    )
    port: int = Field(
        default=8000,
        description="Port to run the agent on",
    )


settings = Settings()
