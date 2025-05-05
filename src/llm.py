"""
Modulo que contiene a nuestr agente cuenta chistes
"""

from typing import cast

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import (
    ChatPromptTemplate,
)
from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field, PrivateAttr


class JokeOutput(BaseModel):
    """
    Chiste generado
    """

    joke: str = Field(description="Chiste generado")


class JokeTeller(BaseModel):
    model_name: str = Field(
        default="gemma3:4b",
        description="Modelo en Ollama a ser invocado",
    )
    _model: BaseChatModel = PrivateAttr()

    def __init__(self, model_name: str, **kwargs):
        """
        Inicializa el agente

        Args:
            model_name (str): El nombre del modelo en Ollama
        """
        super().__init__(model_name=model_name, **kwargs)
        self._model = ChatOllama(model=model_name)

    async def invoke(self, query: str) -> JokeOutput:
        """
        Invoca el modelo para generar un chiste

        Args:
            query (str): El input del usuario

        Returns:
            (JokeOutput): El chiste generado
        """
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Eres un bot comediante. Los usuarios te van a pedir chistes de cualquier tema que deseen
                    y tu deber es responder con el mejor chiste posible.""",
                ),
                ("user", "{input}"),
            ]
        )

        chain = chat_prompt | self._model.with_structured_output(JokeOutput)

        joke = await chain.ainvoke({"input": query})
        joke = cast(JokeOutput, joke)
        return joke
