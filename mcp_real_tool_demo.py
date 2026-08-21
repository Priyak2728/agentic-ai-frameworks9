import boto3
import json
import requests

# 🔹 Bedrock client
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# 🔹 REAL TOOL (Weather API)
def get_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = requests.get(url)
    response.encoding = "utf-8"   
    return response.text

# 🔹 User input
user_input = "What is the weather in Mumbai?"

# 🔹 Prompt
prompt = f"""
You are an AI assistant.

If the user asks about weather, respond ONLY with:
CALL_TOOL: get_weather(city_name)

User: {user_input}
"""

# 🔹 Call Bedrock
body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 200,
    "messages": [
        {
            "role": "user",
            "content": [{"type": "text", "text": prompt}]
        }
    ]
})

response = client.invoke_model(
    modelId="anthropic.claude-3-haiku-20240307-v1:0",
    body=body,
    contentType="application/json",
    accept="application/json"
)

result = json.loads(response["body"].read())
output = result["content"][0]["text"]

print("\n Model Decision:\n", output)

# 🔹 Detect tool call
if "CALL_TOOL" in output:
    print("\n Calling REAL API...\n")
    weather = get_weather("Mumbai")
    print(" Weather Output:\n", weather)