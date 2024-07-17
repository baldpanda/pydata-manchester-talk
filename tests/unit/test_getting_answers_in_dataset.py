from pydata_manchester_talk.utility import read_natural_questions_data, get_long_answer



class TestGettingLongAnswer:


    def test_should_get_long_answer_where_exists(self):

        # Arrange
        test_data = read_natural_questions_data("./data/subset_training_data.jsonl")
        test_observation = test_data[1]
        expected_answer = 'Tracy McConnell'

        # Act
        actual_response = get_long_answer(test_observation)

        # Assert
        assert expected_answer in actual_response