from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import Chroma


class ChromaDatabase:
    def __init__(
        self,
        chroma_path: str,
        bedrock_client,
        model_id: str = "amazon.titan-embed-text-v1",
    ):
        self.chroma_path = chroma_path
        self.model_id = model_id
        self.embeddings = BedrockEmbeddings(client=bedrock_client, model_id=model_id)
        self.db = Chroma(
            persist_directory=chroma_path, embedding_function=self.embeddings
        )

    def get_existing_ids(self):
        existing_items = self.db.get(include=[])
        return set(existing_items["ids"])

    def add_documents(self, chunks, chunk_ids):
        self.db.add_documents(chunks, ids=chunk_ids)

    def get_chroma_db(self):
        return self.db
