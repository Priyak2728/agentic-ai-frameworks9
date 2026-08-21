# research_agent_server.py

from fastapi import FastAPI
import uvicorn
import boto3
import json

app = FastAPI()

client = boto3.client("bedrock-runtime", region_name="us-east-1")

@app.post("/task")
async def handle_task(data: dict):
    topic = data.get("input")

    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "messages": [{
            "role": "user",
            "content": [{
                "type": "text",
                "text": f"Give key points about: {topic}"
            }]
        }]
    })

    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=body
    )

    result = json.loads(response["body"].read())

    return {
        "output": result["content"][0]["text"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)