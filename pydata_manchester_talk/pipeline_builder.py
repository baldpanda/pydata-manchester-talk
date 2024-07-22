from haystack import Document, Pipeline
from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder, SentenceTransformersTextEmbedder)
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy

class DataIngestionPipelineBuilder:
    def __init__(self, document_store):
        self.document_embedder = SentenceTransformersDocumentEmbedder(model="sentence-transformers/all-MiniLM-L6-v2")
        self.document_writer = DocumentWriter(document_store=document_store, policy=DuplicatePolicy.SKIP)
        self.pipeline = Pipeline()

    def build_pipeline(self):
        self.pipeline.add_component(instance=self.document_embedder, name="document_embedder")
        self.pipeline.add_component(instance=self.document_writer, name="document_writer")

        self.pipeline.connect("document_embedder.documents", "document_writer.documents")

    def get_pipeline(self):
        return self.pipeline
    
    def run_pipeline(self, docs_to_be_ingested):
        self.pipeline.run({"document_embedder": {"documents": docs_to_be_ingested}})