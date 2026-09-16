from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def generate_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding for a single text.
        """

        embedding = self.model.encode(
            text,
            convert_to_numpy=True,
        )

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.
        """

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True,
        )

        return embeddings.tolist()