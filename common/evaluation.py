"""Lightweight evaluation layer for chat responses.

Replace the implementation later with Azure AI Foundry evaluators without
changing the chat/agent code because the agent depends on the interface only.
"""

from abc import ABC, abstractmethod


class ResponseEvaluator(ABC):
    """Contract for evaluating an AI response."""

    @abstractmethod
    async def evaluate(
        self,
        question: str,
        answer: str,
        context: str = "",
    ) -> dict:
        raise NotImplementedError


class BasicResponseEvaluator(ResponseEvaluator):
    """Simple baseline evaluator for local development."""

    async def evaluate(
        self,
        question: str,
        answer: str,
        context: str = "",
    ) -> dict:
        return {
            "answer_present": bool(answer.strip()),
            "question_present": bool(question.strip()),
            "grounding_context_used": bool(context.strip()),
            "answer_length": len(answer),
        }
