# file: with_langchain.py

from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage

# 🔹 Initialize Bedrock LLM (Claude)
llm = ChatBedrock( #wrapper for Bedrock Runtime client
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1"
)

# 🔹 Input prompt
prompt = "Explain Agentic AI in simple terms"

# 🔹 Invoke model (NO manual JSON, NO parsing)
response = llm.invoke([
    HumanMessage(content=prompt)
])

# 🔹 Output
print("\nResponse:\n")
print(response.content)