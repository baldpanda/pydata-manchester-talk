from haystack import Document
import json


def get_long_answer(document):
    document_text = document.get("document_text")
    annotations = document.get("annotations")
    long_answer = document_text.split(" ")[
        annotations[0]
        .get("long_answer")
        .get("start_token") : annotations[0]
        .get("long_answer")
        .get("end_token")
    ]
    return " ".join(long_answer)


def get_short_answer(document):
    document_text = document.get("document_text")
    annotations = document.get("annotations")
    return document_text.split(" ")[
        annotations[0]
        .get("short_answers")[0]
        .get("start_token") : annotations[0]
        .get("short_answers")[0]
        .get("end_token")
    ]


def read_natural_questions_data(file_path):
    wiki_docs = []
    with open(file_path, "r") as file:
        for i, line in enumerate(file):
            wiki_docs.append(json.loads(line))

    return wiki_docs


def get_ground_truth_chunks_for_index(document_chunks, long_answer):
    """Gets the ground truth chunks"""
    chunks_containing_long_answer = []
    if long_answer.strip(" ") == "":
        return []
    for chunk in document_chunks:
        if long_answer in chunk.content:
            chunks_containing_long_answer.append(chunk)
    return chunks_containing_long_answer


def get_ground_truth_chunks(documents, document_splitter):
    document_chunks = []
    for doc in documents:
        doc_to_be_split = Document(content=doc["document_text"])
        document_chunks.append(document_splitter.run([doc_to_be_split]))
    ground_truth_chunks = []
    for doc_index in range(0, 10):
        chunks = document_chunks[doc_index].get("documents")
        ground_truth_answer = get_long_answer(documents[doc_index])
        ground_truth_chunks.append(
            get_ground_truth_chunks_for_index(chunks, ground_truth_answer)
        )
    return ground_truth_chunks
