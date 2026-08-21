# file: strands_resume_workflow.py

from strands import Agent
from strands.models import BedrockModel

# 🔹 Model (FIXED ID)
model = BedrockModel(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="us-east-1"
)

# 🔹 Agent
agent = Agent(
    system_prompt="You are a professional career assistant.",
    model=model
)

# 🔹 Input
resume = """
Priya is a data analyst with experience in Python, SQL, and AWS.
She has worked on machine learning models and dashboards.
"""

# 🔹 Step 1
step1 = agent(f"Extract key skills from this resume:\n{resume}")
print("\n Skills:\n", step1)

# 🔹 Step 2
step2 = agent(f"Create a short professional summary using these skills:\n{step1}")
print("\n Summary:\n", step2)

# 🔹 Step 3
step3 = agent(f"Suggest improvements for this profile:\n{step2}")
print("\n Improvements:\n", step3)