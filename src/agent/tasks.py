"""
Este modulo define el gestor de tareas del agente.
"""

from collections.abc import AsyncIterable

from common.server.task_manager import InMemoryTaskManager
from common.types import (
    Artifact,
    JSONRPCResponse,
    Message,
    SendTaskRequest,
    SendTaskResponse,
    SendTaskStreamingRequest,
    SendTaskStreamingResponse,
    Task,
    TaskState,
    TaskStatus,
    TextPart,
)

from agent.llm import JokeTeller


class AgentTaskManager(InMemoryTaskManager):
    """
    Gestor de tareas del agente.
    """

    def __init__(self, model_name: str):
        """
        Inicializa el gestor de tareas.

        Args:
            model_name (str): Nombre del modelo a usar.
        """
        super().__init__()
        self.model_name = model_name
        self.joke_teller = JokeTeller(model_name=model_name)

    async def on_send_task(self, request: SendTaskRequest) -> SendTaskResponse:
        """
        Maneja la recepción de una solicitud de ejecución de una tarea.

        Args:
            request (SendTaskRequest): Solicitud de ejecución de una tarea.

        Returns:
            (SendTaskResponse): Respuesta a la solicitud de ejecución de una tarea.
        """
        # Ingresa la tarea en el gestor de tareas en memoria
        await self.upsert_task(request.params)

        task_id = request.params.id
        # Nuestra lógica personalizada que simplemente marca la tarea como completa
        # y devuelve el texto
        if len(request.params.message.parts) < 0:
            raise ValueError("No text received")

        if not isinstance(request.params.message.parts[0], TextPart):
            raise ValueError("Invalid message part type")

        response = await self.joke_teller.invoke(request.params.message.parts[0].text)

        task = await self._update_task(
            task_id=task_id,
            task_state=TaskState.COMPLETED,
            response_text=f"on_send_task received: {response.joke}",
        )

        # Send the response
        return SendTaskResponse(id=request.id, result=task)

    async def on_send_task_subscribe(
        self, request: SendTaskStreamingRequest
    ) -> AsyncIterable[SendTaskStreamingResponse] | JSONRPCResponse:
        """
        Maneja la suscripción a la recepción de tareas.

        Args:
            request (SendTaskStreamingRequest): Solicitud de suscripción a la recepción de tareas.

        Returns:
            (AsyncIterable[SendTaskStreamingResponse] | JSONRPCResponse): Respuesta a la solicitud de suscripción a la recepción de tareas.

        Raises:
            NotImplementedError: Si no está implementado.
        """
        raise NotImplementedError("Not implemented")

    async def _update_task(
        self,
        task_id: str,
        task_state: TaskState,
        response_text: str,
    ) -> Task:
        """
        Actualiza una tarea.

        Args:
            task_id (str): ID de la tarea.
            task_state (TaskState): Estado de la tarea.
            response_text (str): Texto de la respuesta.

        Returns:
            (Task): Tarea actualizada.
        """
        task = self.tasks[task_id]
        agent_response_parts = [
            {
                "type": "text",
                "text": response_text,
            }
        ]
        task.status = TaskStatus(
            state=task_state,
            message=Message(
                role="agent",
                parts=[TextPart(text=part["text"]) for part in agent_response_parts],
            ),
        )
        task.artifacts = [
            Artifact(
                parts=[TextPart(text=part["text"]) for part in agent_response_parts],
            )
        ]
        return task
