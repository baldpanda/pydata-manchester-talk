import json

def get_long_answer(document):
    document_text = document.get("document_text")
    annotations = document.get("annotations")
    long_answer = document_text.split(" ")[annotations[0].get("long_answer").get("start_token"): annotations[0].get("long_answer").get("end_token")]
    return " ".join(long_answer)


def get_short_answer(document):
    document_text = document.get("document_text")
    annotations = document.get("annotations")
    return document_text.split(" ")[annotations[0].get("short_answers")[0].get("start_token"): annotations[0].get("short_answers")[0].get("end_token")]

def read_natural_questions_data(file_path):
    wiki_docs = []
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            wiki_docs.append(json.loads(line))

    return wiki_docs

def get_ground_truth_chunks(document_chunks, long_answer):
    """Gets the ground truth chunks"""
    chunks_containing_long_answer = []
    if long_answer.strip(" ") == "":
        return []
    for chunk in document_chunks:
        if long_answer in chunk.content:
            chunks_containing_long_answer.append(chunk)
    return chunks_containing_long_answer