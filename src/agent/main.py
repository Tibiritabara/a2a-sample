"""
Este modulo lanza el servidor que implementa el agente.
"""

import click
from common.types import AgentCapabilities, AgentCard, AgentSkill

from agent.logs import logger
from agent.settings import settings


@click.command()
@click.option(
    "--host",
    default="localhost",
    help="Host to run the agent on",
)
@click.option(
    "--port",
    default=8000,
    help="Port to run the agent on",
)
def main(host: str, port: int):
    """
    Lanza el servidor que implementa el agente.

    Args:
        host: Host to run the agent on
        port: Port to run the agent on
    """
    skill = AgentSkill(
        id="agente-comediante-cuenta-chistes",
        name="Cuenta chistes",
        description="Cuenta chistes para entretener a la audiencia",
        tags=["joke", "comedy", "funny"],
        examples=[
            "Cuentame un chiste",
            "Dame un chiste",
            "Hazme reir con un chiste",
        ],
        inputModes=["text"],
        outputModes=["text"],
    )

    capabilities = AgentCapabilities()
    agent_card = AgentCard(
        name="Agente Comediante",
        description="Agente que cuenta chistes",
        url=f"http://{host}:{port}",
        version="0.1.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=capabilities,
        skills=[skill],
    )
    logger.info(agent_card)


if __name__ == "__main__":
    main(host=settings.host, port=settings.port)
