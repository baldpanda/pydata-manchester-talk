from haystack import Pipeline
from haystack.components.builders import AnswerBuilder, PromptBuilder
from haystack.components.embedders import (
    SentenceTransformersDocumentEmbedder,
    SentenceTransformersTextEmbedder,
)
from haystack.components.generators import OpenAIGenerator
from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.evaluators.faithfulness import FaithfulnessEvaluator
from haystack.components.evaluators.document_mrr import DocumentMRREvaluator


class DataIngestionPipelineBuilder:
    def __init__(self, document_store):
        self.document_embedder = SentenceTransformersDocumentEmbedder(
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.document_writer = DocumentWriter(
            document_store=document_store, policy=DuplicatePolicy.SKIP
        )
        self.document_splitter = DocumentSplitter(
            split_by="word", split_length=500, split_overlap=150
        )
        self.pipeline = Pipeline()

    def build_pipeline(self):
        self.pipeline.add_component(
            instance=self.document_embedder, name="document_embedder"
        )
        self.pipeline.add_component(
            instance=self.document_writer, name="document_writer"
        )

        self.pipeline.connect(
            "document_embedder.documents", "document_writer.documents"
        )

    def get_pipeline(self):
        return self.pipeline

    def run_pipeline(self, docs_to_be_ingested):
        self.pipeline.run({"document_embedder": {"documents": docs_to_be_ingested}})

    def run_pipeline_with_chunking(self, docs_to_be_ingested):
        self.pipeline.run({"document_splitter": {"documents": docs_to_be_ingested}})

    def add_preprocessor_to_pipeline(self):
        self.pipeline.add_component(
            instance=self.document_splitter, name="document_splitter"
        )
        self.pipeline.connect(
            "document_splitter.documents", "document_embedder.documents"
        )

    def get_document_splitter(self):
        return self.document_splitter


class RagPipelineBuilder:
    def __init__(self, document_store, prompt_template):
        self.document_store = document_store
        self.pipeline = Pipeline()
        self.prompt_template = prompt_template

    def build_pipeline(self):

        # Responsuible for embedding the query text
        self.pipeline.add_component(
            "query_embedder",
            SentenceTransformersTextEmbedder(
                model="sentence-transformers/all-MiniLM-L6-v2"
            ),
        )
        # Responsible for retrieving the top k documents
        self.pipeline.add_component(
            "retriever", InMemoryEmbeddingRetriever(self.document_store, top_k=3)
        )
        # Responsible for building the prompt with the required parameters (show prompt)
        self.pipeline.add_component(
            "prompt_builder", PromptBuilder(template=self.prompt_template)
        )
        # Responsible for generating the answer with the given prompt
        self.pipeline.add_component("generator", OpenAIGenerator(model="gpt-3.5-turbo"))
        #  Useful for gathering the answers and metadata from the different parts of the pipeline
        self.pipeline.add_component("answer_builder", AnswerBuilder())

        self.pipeline.connect("query_embedder", "retriever.query_embedding")
        self.pipeline.connect("retriever", "prompt_builder.documents")
        self.pipeline.connect("prompt_builder", "generator")
        self.pipeline.connect("generator.replies", "answer_builder.replies")
        self.pipeline.connect("generator.meta", "answer_builder.meta")
        self.pipeline.connect("retriever", "answer_builder.documents")

    def get_pipeline(self):
        return self.pipeline

    def run_pipeline(self, query):
        return self.pipeline.run(
            {
                "query_embedder": {"text": query},
                "prompt_builder": {"question": query},
                "answer_builder": {"query": query},
            }
        )


class EvaluationPipeline:

    def __init__(self):
        self.pipeline = Pipeline()

    def build_pipeline(self):
        self.pipeline.add_component("doc_mrr_evaluator", DocumentMRREvaluator())
        self.pipeline.add_component("faithfulness", FaithfulnessEvaluator())

    def run_pipeline(self, questions, retrieved_docs, ground_truth_docs, rag_answers):
        return self.pipeline.run(
            {
                "doc_mrr_evaluator": {
                    "ground_truth_documents": list(
                        d.get("ground_truth_chunks") for d in ground_truth_docs
                    ),
                    "retrieved_documents": retrieved_docs,
                },
                "faithfulness": {
                    "questions": list(questions),
                    "contexts": list(
                        d.get("ground_truth_chunks") for d in ground_truth_docs
                    ),
                    "predicted_answers": rag_answers,
                },
            }
        )
