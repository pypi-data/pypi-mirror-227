import pytest
from tensorflow.python.keras.models import load_model

import sys
sys.path.append("C:\\Users\\flori\\Desktop\\Programming\\Python\\neuralintents\\neuralintents")
from assistants import BasicAssistant


def test_initialize_with_valid_intents_data():
    assistant = BasicAssistant("C:\\Users\\flori\\Desktop\\Programming\\Python\\neuralintents\\neuralintents\\intents.json")
    assert assistant.intents_data is not None

    intents_data = {
        "intents": [
            {
                "tag": "greeting",
                "patterns": ["Hi", "Hello", "Hey"],
                "responses": ["Hello!", "Hi there!", "Greetings!"]
            }
        ]
    }
    assistant = BasicAssistant(intents_data)
    assert assistant.intents_data is not None

    with pytest.raises(FileNotFoundError):
        BasicAssistant("non_existent_file.json")


def test_fit_model():
    assistant = BasicAssistant("C:\\Users\\flori\\Desktop\\Programming\\Python\\neuralintents\\neuralintents\\intents.json")
    assistant.fit_model()
    assert assistant.model is not None


def test_process_input(monkeypatch):
    assistant = BasicAssistant("C:\\Users\\flori\\Desktop\\Programming\\Python\\neuralintents\\neuralintents\\intents.json")
    assistant.fit_model()

    def mock_method():
        return "Mock method called."

    assistant.method_mappings["greeting"] = mock_method

    input_text = "Hi there!"
    response = assistant.process_input(input_text)
    assert response in ["Hello!", "Good to see you again!", "Hi there, how can I help?"]

    input_text = "What's the weather like today?"
    response = assistant.process_input(input_text)
    assert response == "I don't understand. Please try again."


def test_initialize_with_empty_intents_data(mocker):
    intents_data = {}
    basic_assistant = BasicAssistant(intents_data=intents_data)
    assert basic_assistant.intents_data == intents_data

    intents_data_file = mocker.Mock()
    mocker.patch("json.load", return_value=intents_data)
    basic_assistant = BasicAssistant(intents_data=intents_data_file)
    assert basic_assistant.intents_data == intents_data


def test_fit_model_with_no_hidden_layers():
    intents_data = {
        "intents": [
            {
                "tag": "greeting",
                "patterns": ["Hi", "Hello", "Hey"],
                "responses": ["Hello!", "Hi there!", "Greetings!"]
            },
            {
                "tag": "goodbye",
                "patterns": ["Bye", "See you later", "Goodbye"],
                "responses": ["Goodbye!", "See you later!", "Take care!"]
            }
        ]
    }
    basic_assistant = BasicAssistant(intents_data=intents_data)
    basic_assistant.fit_model()
    assert basic_assistant.model is not None


def test_fit_model_with_none_optimizer():
    intents_data = {
        "intents": [
            {
                "tag": "greeting",
                "patterns": ["Hi", "Hello", "Hey"],
                "responses": ["Hello!", "Hi there!", "Greetings!"]
            },
            {
                "tag": "goodbye",
                "patterns": ["Bye", "See you later", "Goodbye"],
                "responses": ["Goodbye!", "See you later!", "Take care!"]
            }
        ]
    }
    basic_assistant = BasicAssistant(intents_data=intents_data)
    basic_assistant.fit_model(optimizer=None)
    assert basic_assistant.model is not None


def test_save_model(mocker):
    mock_model = mocker.Mock()
    mock_words = mocker.Mock()
    mock_intents = mocker.Mock()
    mock_history = mocker.Mock()
    assistant = BasicAssistant(intents_data={}, model_name="test_model")
    assistant.model = mock_model
    assistant.words = mock_words
    assistant.intents = mock_intents
    assistant.history = mock_history
    pickle_dump_mock = mocker.patch("pickle.dump")
    model_save_mock = mocker.patch.object(mock_model, "save")

    assistant.save_model()

    pickle_dump_mock.assert_any_call(mock_words, mocker.ANY)
    pickle_dump_mock.assert_any_call(mock_intents, mocker.ANY)
    model_save_mock.assert_called_once_with("test_model.h5", mock_history)


def test_load_model(mocker):
    mock_model = mocker.Mock()
    mock_words = ["word1", "word2"]
    mock_intents = ["intent1", "intent2"]
    assistant = BasicAssistant(intents_data={}, model_name="test_model")
    assistant.model = mock_model
    pickle_load_mock = mocker.patch("pickle.load")
    pickle_load_mock.side_effect = [mock_words, mock_intents]
    load_model_mock = mocker.patch.object(load_model, "__call__")

    assistant.load_model()

    pickle_load_mock.assert_any_call(mocker.ANY)
    pickle_load_mock.assert_any_call(mocker.ANY)
    load_model_mock.assert_called_once_with("test_model.h5")


def test_shuffle_training_data(mocker):
    mock_intents_data = {
        "intents": [
            {
                "tag": "greeting",
                "patterns": ["Hi", "Hello", "Hey"],
                "responses": ["Hello!", "Hi there!", "Greetings!"]
            },
            {
                "tag": "goodbye",
                "patterns": ["Bye", "See you later", "Goodbye"],
                "responses": ["Goodbye!", "See you later!", "Take care!"]
            }
        ]
    }
    assistant = BasicAssistant(intents_data=mock_intents_data)
    shuffle_mock = mocker.patch("random.shuffle")

    assistant._prepare_intents_data()

    shuffle_mock.assert_called_once_with(mocker.ANY)
