# writer_agent_server.py

from fastapi import FastAPI
import requests
import uvicorn
import boto3
import json

app = FastAPI()

client = boto3.client("bedrock-runtime", region_name="us-east-1")

@app.post("/task")
async def handle_task(data: dict):
    topic = data.get("input")

    # 🔹 Call Research Agent
    res = requests.post(
        "http://127.0.0.1:8001/task",
        json={"input": topic}
    )

    research_data = res.json()["output"]

    # 🔹 Generate final explanation
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 200,
        "messages": [{
            "role": "user",
            "content": [{
                "type": "text",
                "text": f"Explain simply:\n{research_data}"
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
    uvicorn.run(app, host="127.0.0.1", port=8002)