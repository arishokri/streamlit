import argparse
import json
from argparse import RawTextHelpFormatter
import requests
from typing import Optional
import warnings

try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn(
        "Langflow provides a function to help you upload files to the flow. Please install langflow to use it."
    )
    upload_file = None

BASE_API_URL = "http://127.0.0.1:7860"
FLOW_ID = "7249a5c9-5a0f-496e-9cb7-2c20fe6e4fff"
ENDPOINT = ""  # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
    "OpenAIModel-M0qvB": {
        "api_key": "OpenAI_API_Key",
        "input_value": "",
        "json_mode": False,
        "max_tokens": None,
        "model_kwargs": {},
        "model_name": "gpt-4o-mini",
        "openai_api_base": "",
        "output_schema": {},
        "seed": 1,
        "stream": True,
        "system_message": "",
        "temperature": 0.2,
    }
}


def run_flow(
    message: str,
    endpoint: str,
    output_type: str = "chat",
    input_type: str = "chat",
    tweaks: Optional[dict] = None,
    api_key: Optional[str] = None,
) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/api/v1/run/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()


# parser = argparse.ArgumentParser(description="""Run a flow with a given message and optional tweaks.
# Run it like: python <your file>.py "your message here" --endpoint "your_endpoint" --tweaks '{"key": "value"}'""",
#     formatter_class=RawTextHelpFormatter)
# parser.add_argument("message", type=str, help="The message to send to the flow")
# parser.add_argument("--endpoint", type=str, default=ENDPOINT or FLOW_ID, help="The ID or the endpoint name of the flow")
# parser.add_argument("--tweaks", type=str, help="JSON string representing the tweaks to customize the flow", default=json.dumps(TWEAKS))
# parser.add_argument("--api_key", type=str, help="API key for authentication", default=None)
# parser.add_argument("--output_type", type=str, default="chat", help="The output type")
# parser.add_argument("--input_type", type=str, default="chat", help="The input type")
# parser.add_argument("--upload_file", type=str, help="Path to the file to upload", default=None)
# parser.add_argument("--components", type=str, help="Components to upload the file to", default=None)

# args = parser.parse_args()
# try:
#     tweaks = json.loads(args.tweaks)
# except json.JSONDecodeError:
#     raise ValueError("Invalid tweaks JSON string")

# if args.upload_file:
#     if not upload_file:
#         raise ImportError("Langflow is not installed. Please install it to use the upload_file function.")
#     elif not args.components:
#         raise ValueError("You need to provide the components to upload the file to.")
#     tweaks = upload_file(file_path=args.upload_file, host=BASE_API_URL, flow_id=ENDPOINT, components=args.components, tweaks=tweaks)

message = "How old was Elon when he moved out of South Africa?"

response = run_flow(message=message, endpoint=FLOW_ID)

returned = response["outputs"][0]["outputs"][0]["results"]["message"]["data"]["text"]
print(type(returned), "\n\n")
print(returned, "\n\n")
print(json.dumps(response, indent=2))

