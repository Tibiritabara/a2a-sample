"""
Este modulo lanza el servidor que implementa el agente.
"""

from common.server import A2AServer
from common.types import AgentCapabilities, AgentCard, AgentSkill

from agent.logs import logger
from agent.settings import settings
from agent.tasks import AgentTaskManager


def main(host: str, port: int, model: str):
    """
    Lanza el servidor que implementa el agente.

    Args:
        host: Host to run the agent on
        port: Port to run the agent on
        model: Model to run the agent on
    """
    # Definimos los skills del agente
    # En este caso, solo tenemos un skill: contar chistes
    skill = AgentSkill(
        id="agente-comediante-cuenta-chistes",
        name="Cuenta chistes",
        description="Cuenta chistes para entretener a la audiencia",
        tags=["joke", "comedy", "funny"],
        examples=[
            "Cuentame un chiste de autos",
            "Dame un chiste de colombianos",
            "Hazme reir con un chiste de familias",
        ],
        inputModes=["text"],
        outputModes=["text"],
    )

    capabilities = AgentCapabilities()

    # Definimos la card del agente donde se describe el agente y sus skills
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

    # Se inicializa el gestor de tareas
    task_manager = AgentTaskManager(model_name=model)

    # Se inicializa el servidor
    server = A2AServer(
        agent_card=agent_card,
        task_manager=task_manager,
        host=host,
        port=port,
    )
    server.start()


if __name__ == "__main__":
    main(
        host=settings.host,
        port=settings.port,
        model=settings.model,
    )
