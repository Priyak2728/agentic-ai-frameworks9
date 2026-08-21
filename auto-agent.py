

import json
import boto3
from datetime import datetime

# =========================================================
# AWS CLIENTS
# =========================================================

REGION = "us-east-1"   # change if needed

bedrock_runtime = boto3.client(
    service_name="bedrock-runtime",
    region_name=REGION
)

s3 = boto3.client(
    "s3",
    region_name=REGION
)

lambda_client = boto3.client(
    "lambda",
    region_name=REGION
)

ec2 = boto3.client(
    "ec2",
    region_name=REGION
)

# =========================================================
# MEMORY
# =========================================================

memory_store = []

def save_memory(item):
    memory_store.append(item)

def get_memory():
    return memory_store

# =========================================================
# BEDROCK MODEL CALL
# =========================================================

def invoke_bedrock(prompt):

    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "maxTokens": 1000,
            "temperature": 0.5,
            "topP": 0.9
        }
    }

    response = bedrock_runtime.invoke_model(
        modelId="amazon.nova-pro-v1:0",
        body=json.dumps(body)
    )

    response_body = json.loads(
        response["body"].read()
    )

    final_response = (
        response_body["output"]["message"]["content"][0]["text"]
    )

    return final_response

# =========================================================
# AWS TOOLS
# =========================================================

def list_s3_buckets():

    response = s3.list_buckets()

    buckets = [
        bucket["Name"]
        for bucket in response["Buckets"]
    ]

    return buckets


def list_lambda_functions():

    response = lambda_client.list_functions()

    functions = [
        fn["FunctionName"]
        for fn in response["Functions"]
    ]

    return functions


def list_ec2_instances():

    response = ec2.describe_instances()

    instances = []

    for reservation in response["Reservations"]:

        for instance in reservation["Instances"]:

            instances.append({
                "InstanceId": instance.get("InstanceId"),
                "State": instance.get("State", {}).get("Name"),
                "Type": instance.get("InstanceType")
            })

    return instances

# =========================================================
# AUTONOMOUS TOOL ROUTER
# =========================================================

def aws_tool_router(task):

    task_lower = task.lower()

    # -----------------------------------------------------

    if "s3" in task_lower or "bucket" in task_lower:

        print("\n[TOOL] S3 TOOL ACTIVATED")

        result = list_s3_buckets()

        return {
            "tool": "S3",
            "result": result
        }

    # -----------------------------------------------------

    elif "lambda" in task_lower:

        print("\n[TOOL] LAMBDA TOOL ACTIVATED")

        result = list_lambda_functions()

        return {
            "tool": "Lambda",
            "result": result
        }

    # -----------------------------------------------------

    elif "ec2" in task_lower or "instance" in task_lower:

        print("\n[TOOL] EC2 TOOL ACTIVATED")

        result = list_ec2_instances()

        return {
            "tool": "EC2",
            "result": result
        }

    # -----------------------------------------------------

    else:

        print("\n[TOOL] GENERAL ANALYSIS")

        return {
            "tool": "General",
            "result": "No direct AWS tool matched"
        }

# =========================================================
# AUTONOMOUS PLANNER
# =========================================================

def create_plan(goal):

    goal_lower = goal.lower()

    plan = []

    # -----------------------------------------------------

    if "s3" in goal_lower or "bucket" in goal_lower:

        plan.append("Analyze S3 buckets")
        plan.append("Review bucket usage")
        plan.append("Generate optimization recommendations")

    # -----------------------------------------------------

    elif "lambda" in goal_lower:

        plan.append("Inspect Lambda functions")
        plan.append("Review Lambda configurations")
        plan.append("Generate Lambda recommendations")

    # -----------------------------------------------------

    elif "ec2" in goal_lower:

        plan.append("Inspect EC2 instances")
        plan.append("Analyze instance states")
        plan.append("Generate EC2 recommendations")

    # -----------------------------------------------------

    elif "security" in goal_lower:

        plan.append("Inspect AWS resources")
        plan.append("Identify security risks")
        plan.append("Generate remediation plan")

    # -----------------------------------------------------

    else:

        plan.append("Understand AWS environment")
        plan.append("Analyze available resources")
        plan.append("Generate cloud insights")

    return plan

# =========================================================
# AUTONOMOUS AGENT
# =========================================================

def autonomous_agent(user_goal):

    print("\n================================================")
    print("AWS AUTONOMOUS AGENT STARTED")
    print("================================================\n")

    print(f"USER GOAL:\n{user_goal}\n")

    # =====================================================
    # STEP 1 — PLAN
    # =====================================================

    plan = create_plan(user_goal)

    print("AUTONOMOUS PLAN:\n")

    for idx, step in enumerate(plan, start=1):
        print(f"{idx}. {step}")

    # =====================================================
    # STEP 2 — EXECUTE
    # =====================================================

    execution_results = []

    print("\n================================================")
    print("EXECUTION STARTED")
    print("================================================")

    for step in plan:

        print(f"\n[EXECUTING] {step}")

        tool_output = aws_tool_router(step)

        result = {
            "step": step,
            "tool_used": tool_output["tool"],
            "output": tool_output["result"]
        }

        execution_results.append(result)

        save_memory(result)

        print("[SUCCESS] STEP COMPLETED")

    # =====================================================
    # STEP 3 — AI REASONING
    # =====================================================

    final_prompt = f"""
You are an advanced autonomous AWS cloud agent.

Current Date:
{datetime.now()}

User Goal:
{user_goal}

Execution Results:
{json.dumps(execution_results, indent=2)}

Memory:
{json.dumps(get_memory(), indent=2)}

Generate:
1. Detailed AWS analysis
2. Key findings
3. Risks
4. Optimization suggestions
5. Security recommendations
6. Cost optimization ideas
7. Next best actions
"""

    print("\n================================================")
    print("AMAZON NOVA PRO THINKING...")
    print("================================================\n")

    final_response = invoke_bedrock(final_prompt)

    # =====================================================
    # STEP 4 — FINAL RESPONSE
    # =====================================================

    print("\n================================================")
    print("FINAL AUTONOMOUS RESPONSE")
    print("================================================\n")

    print(final_response)

    print("\n================================================")
    print("AGENT EXECUTION FINISHED")
    print("================================================\n")

# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("\n==============================================")
    print("AMAZON NOVA PRO AUTONOMOUS AWS AGENT")
    print("==============================================")

    user_goal = input("\nEnter your AWS goal: ")

    autonomous_agent(user_goal)