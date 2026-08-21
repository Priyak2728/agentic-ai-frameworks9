# file: without_langchain.py

import boto3
import json

# 🔹 Create Bedrock Runtime client
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# 🔹 Input prompt
prompt = "Explain Agentic AI in simple terms"

# 🔹 Proper Claude request format
body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 200,
    "messages": [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                }
            ]
        }
    ]
})

# 🔹 Invoke model
response = client.invoke_model(
    modelId="anthropic.claude-3-haiku-20240307-v1:0",
    body=body,
    contentType="application/json",
    accept="application/json"
)

# 🔹 Read and parse response
response_body = json.loads(response["body"].read())

# 🔹 Extract output text
output_text = response_body["content"][0]["text"]

print("\n🧠 Response:\n")
print(output_text)