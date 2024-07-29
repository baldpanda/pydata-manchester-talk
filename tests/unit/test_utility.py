import pytest
from pydata_manchester_talk.utility import get_long_answer

class TestGetLongAnswer:
    def test_should_return_long_answer(self):
        # Arrange
        document = {
            "document_text": "This is a sample document",
            "annotations": [
                {
                    "long_answer": {
                        "start_token": 2,
                        "end_token": 4
                    }
                }
            ]
        }
        expected_answer = "a sample"

        # Act
        actual_answer = get_long_answer(document)

        # Assert
        assert actual_answer == expected_answer

    def test_should_return_empty_string_when_no_long_answer(self):
        # Arrange
        document = {
            "document_text": "This is a sample document",
            "annotations": []
        }
        expected_answer = ""

        # Act
        actual_answer = get_long_answer(document)

        # Assert
        assert actual_answer == expected_answer

    def test_should_return_empty_string_when_document_text_empty(self):
        # Arrange
        document = {
            "document_text": "",
            "annotations": [
                {
                    "long_answer": {
                        "start_token": 2,
                        "end_token": 4
                    }
                }
            ]
        }
        expected_answer = ""

        # Act
        actual_answer = get_long_answer(document)

        # Assert
        assert actual_answer == expected_answer