from google.cloud import dialogflow
from environs import Env


def detect_intent_texts(session_id, text, language_code="ru"):
    env = Env()
    env.read_env(".env")
    dialogflow_project_id = env("DIALOGFLOW_PROJECT_ID")

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(dialogflow_project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    if not response.query_result.intent.is_fallback:
        return response.query_result.fulfillment_text
