from google.cloud import dialogflow
from environs import Env
import json
from google.api_core.exceptions import InvalidArgument
import argparse
import logging


logger = logging.getLogger("intents_loader")


def read_file_to_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        questions = file.read()
    return json.loads(questions)


def create_intent(display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(DIALOGFLOW_PROJECT_ID)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message]
    )

    intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )


def main(filename):
    logger.warning("Start loading intents into DialogFlow")
    questions = read_file_to_json(filename)
    for topic, training_data in questions.items():
        try:
            create_intent(topic, training_data["questions"], [training_data["answer"]])
            logger.warning(f"{topic} is added")
        except InvalidArgument:
            logger.error(f"{topic} is already exists")


if __name__ == "__main__":
    env = Env()
    env.read_env(".env")

    DIALOGFLOW_PROJECT_ID = env("DIALOGFLOW_PROJECT_ID")

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", metavar="", help="name of file with questions")
    args = parser.parse_args()

    logger.setLevel(logging.WARNING)

    main(args.filename)
