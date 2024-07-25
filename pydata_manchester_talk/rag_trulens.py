from trulens_eval.tru_custom_app import instrument
from haystack.components.embedders import (
    SentenceTransformersTextEmbedder,
)
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack.components.generators import OpenAIGenerator

class RagTrulens:
    def __init__(self, document_store, prompt_template):
        self.document_store = document_store
        self.query_embedder = SentenceTransformersTextEmbedder(
                model="sentence-transformers/all-MiniLM-L6-v2"
            )
        self.query_embedder.warm_up()
        self.prompt_template = prompt_template

    @instrument
    def retrieve(self, query: str) -> list:
        """
        Retrieve relevant text from vector store.
        """
        self.query_embedder.warm_up()
        embedded_query = self.query_embedder.run(text=query).get("embedding")
        retriever = InMemoryEmbeddingRetriever(self.document_store, top_k=3)
        # Flatten the list of lists into a single list
        return retriever.run(query_embedding=embedded_query).get("documents")

    @instrument
    def generate_completion(self, query: str, documents: list) -> str:
        """
        Generate answer from context.
        """
        prompt_builder = PromptBuilder(template=self.prompt_template)
        geneartor =  OpenAIGenerator(model="gpt-3.5-turbo")
        prompt = prompt_builder.run(question=query, documents=documents).get("prompt")
        return geneartor.run(prompt=prompt)

    @instrument
    def query(self, query: str) -> str:
        context_str = self.retrieve(query)
        completion = self.generate_completion(query, context_str)
        return completion