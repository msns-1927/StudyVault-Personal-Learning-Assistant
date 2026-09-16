import chromadb

from backend.config import (
    COLLECTION_NAME,
    VECTOR_DB_DIR,
)


class VectorStore:

    def __init__(
        self,
        collection_name: str = COLLECTION_NAME,
        chroma_path: str = str(VECTOR_DB_DIR),
    ):
        self.client = chromadb.PersistentClient(
            path=chroma_path
        )

        self.collection = (
            self.client.get_or_create_collection(
                name=collection_name
            )
        )

    def add_chunks(
        self,
        chunks: list[dict],
        embeddings: list[list[float]],
        document_id: str,
        filename: str,
        file_hash: str | None = None,
    ) -> int:

        if not chunks:
            return 0

        ids = []
        documents = []
        metadatas = []

        for index, chunk in enumerate(chunks):

            chunk_id = (
                f"{document_id}_{index}"
            )

            ids.append(chunk_id)

            documents.append(
                chunk["text"]
            )

            metadatas.append(
                {
                    "document_id": document_id,
                    "filename": filename,
                    "page": chunk["page"],
                    "chunk_index": chunk[
                        "chunk_index"
                    ],
                    "file_hash": file_hash or "",
                }
            )

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        return len(chunks)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than 0."
            )

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k,
        )

        documents = results.get(
            "documents",
            [[]],
        )[0]

        metadatas = results.get(
            "metadatas",
            [[]],
        )[0]

        distances = results.get(
            "distances",
            [[]],
        )[0]

        ids = results.get(
            "ids",
            [[]],
        )[0]

        retrieved_chunks = []

        for (
            chunk_id,
            document,
            metadata,
            distance,
        ) in zip(
            ids,
            documents,
            metadatas,
            distances,
        ):

            retrieved_chunks.append(
                {
                    "chunk_id": chunk_id,
                    "text": document,
                    "metadata": metadata,
                    "distance": distance,
                }
            )

        return retrieved_chunks

    def count(self) -> int:
        """
        Return the number of stored chunks.
        """

        return self.collection.count()

    def get_documents(self) -> list[dict]:
        """
        Return a list of uploaded documents
        stored in ChromaDB.
        """

        results = self.collection.get(
            include=["metadatas"]
        )

        metadatas = results.get(
            "metadatas",
            [],
        )

        documents = {}

        for metadata in metadatas:

            document_id = metadata[
                "document_id"
            ]

            filename = metadata[
                "filename"
            ]

            if document_id not in documents:

                documents[document_id] = {
                    "document_id": document_id,
                    "filename": filename,
                    "chunks": 0,
                }

            documents[
                document_id
            ]["chunks"] += 1

        return list(
            documents.values()
        )

    def delete_document(
        self,
        document_id: str,
    ) -> int:
        """
        Delete all chunks belonging
        to a document.
        """

        results = self.collection.get(
            where={
                "document_id": document_id
            },
            include=["metadatas"],
        )

        ids = results.get(
            "ids",
            [],
        )

        if not ids:
            return 0

        self.collection.delete(
            ids=ids
        )

        return len(ids)


    def document_hash_exists(self, file_hash: str) -> bool:
        """
        Check whether a document with the given
        SHA-256 hash already exists.
        """

        if not file_hash:
            return False

        results = self.collection.get(
            where={"file_hash": file_hash},
            include=["metadatas"],
        )

        return bool(results.get("ids"))