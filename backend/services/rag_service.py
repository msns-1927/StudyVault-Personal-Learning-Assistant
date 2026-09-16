from backend.services.llm_service import LLMService
from backend.services.retrieval_service import RetrievalService
from backend.services.database import get_messages

from backend.config import RELEVANCE_THRESHOLD

class RAGService:
    def __init__(
        self,
        retrieval_service: RetrievalService | None = None,
        llm_service: LLMService | None = None,
    ):
        self.retrieval_service = (
            retrieval_service
            if retrieval_service is not None
            else RetrievalService()
        )

        self.llm_service = (
            llm_service
            if llm_service is not None
            else LLMService()
        )


    def get_conversation_history(
        self,
        conversation_id: int,
        limit: int = 6,
    ) -> list[dict]:
        messages = get_messages(conversation_id)

        return messages[-limit:]

    def build_prompt(
        self,
        question: str,
        retrieved_chunks: list[dict],
        conversation_history: list[dict] | None = None,
        study_mode: str = "explain",
    ) -> str:
        """
        Build the LLM prompt based on the selected study mode.
        """

        conversation_history = conversation_history or []

        history_parts = []

        for message in conversation_history:
            history_parts.append(
                f"{message['role'].capitalize()}: "
                f"{message['content']}"
            )

        conversation_context = "\n".join(
            history_parts
        )

        if not conversation_context:
            conversation_context = (
                "No previous conversation."
            )

        context_parts = []

        for index, chunk in enumerate(
            retrieved_chunks,
            start=1,
        ):
            metadata = chunk["metadata"]

            context_parts.append(
                f"[Source {index}]\n"
                f"Filename: {metadata['filename']}\n"
                f"Page: {metadata['page']}\n"
                f"Chunk: {metadata['chunk_index']}\n"
                f"Content: {chunk['text']}"
            )

        context = "\n\n---\n\n".join(
            context_parts
        )

        mode_instruction = self.get_study_mode_instruction(
            study_mode
        )

        prompt = f"""
    You are StudyVault, a personal learning assistant.

    Study Mode:
    {study_mode}

    Study Mode Instructions:
    {mode_instruction}

    Conversation History:

    {conversation_context}

    Answer the user's question using ONLY the provided context.

    Rules:
    1. Do not use information that is not present in the context.
    2. If the context does not contain enough information to answer,
    say that you could not find the answer in the uploaded documents.
    3. Explain the answer clearly and simply.
    4. Do not invent facts, sources, or page numbers.
    5. Cite the source after relevant claims using this format:
    [Source: filename, Page: X]
    6. Only cite sources that are actually provided in the context.
    7. Do not create or guess source information.

    Context:

    {context}

    User Question:

    {question}

    Answer:
    """

        return prompt

    def answer(
        self,
        question: str,
        top_k: int = 5,
        conversation_id: int | None = None,
        study_mode: str = "explain",
    ) -> dict:
        if not question.strip():
            raise ValueError("Question cannot be empty.")

        history = []

        if conversation_id is not None:
            history = self.get_conversation_history(
                conversation_id=conversation_id
            )

        # Build a context-aware search query.
        search_query = question

        if history:
            history_text = "\n".join(
                f"{message['role']}: {message['content']}"
                for message in history
            )

            search_query = (
                f"Conversation context:\n"
                f"{history_text}\n\n"
                f"Current question:\n"
                f"{question}"
            )

        retrieved_chunks = self.retrieval_service.retrieve(
            query=search_query,
            top_k=top_k,
        )

        if not retrieved_chunks:
            return {
                "question": question,
                "answer": (
                    "I could not find enough information "
                    "in the uploaded documents to answer this question."
                ),
                "sources": [],
            }

        best_distance = retrieved_chunks[0]["distance"]

        if best_distance > RELEVANCE_THRESHOLD:
            return {
                "question": question,
                "answer": (
                    "I could not find enough relevant information "
                    "in the uploaded documents to answer this question."
                ),
                "sources": [],
            }

        prompt = self.build_prompt(
            question=question,
            retrieved_chunks=retrieved_chunks,
            conversation_history=history,
            study_mode=study_mode,
        )

        answer = self.llm_service.generate(prompt)

        sources = []
        seen_sources = set()

        for chunk in retrieved_chunks:
            metadata = chunk["metadata"]

            source_key = (
                metadata["filename"],
                metadata["page"],
            )

            if source_key in seen_sources:
                continue

            seen_sources.add(source_key)

            sources.append(
                {
                    "filename": metadata["filename"],
                    "page": metadata["page"],
                }
            )

        return {
            "question": question,
            "answer": answer,
            "sources": sources,
        }


    def get_study_mode_instruction(
        self,
        study_mode: str,
    ) -> str:
        """
        Return instructions for the selected study mode.
        """

        instructions = {
            "explain": """
    Explain the concept clearly for a student.

    Start with a simple explanation.
    Then explain the important details.
    Use examples only when they are supported
    by the provided context.
    """,

            "summary": """
    Summarize the provided information concisely.

    Focus on the main ideas, important facts,
    definitions, and conclusions.

    Use bullet points where appropriate.
    """,

            "quiz": """
    Create a short quiz based only on the provided context.

    Generate 5 questions.
    Include the answers after the questions.
    Do not introduce information that is not
    present in the context.
    """,

            "flashcards": """
    Create study flashcards from the provided context.

    Format them as:

    Flashcard 1
    Question:
    Answer:

    Create 5 useful flashcards.
    """,

            "key_points": """
    Extract the most important learning points
    from the provided context.

    Use clear bullet points.
    Focus on definitions, concepts,
    important facts, and relationships.
    """,
        }

        return instructions.get(
            study_mode,
            instructions["explain"],
        )