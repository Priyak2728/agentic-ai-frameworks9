import json
import boto3

REGION = "us-east-1"

bedrock = boto3.client(
    "bedrock-runtime",
    region_name=REGION
)

ec2 = boto3.client("ec2", region_name=REGION)
s3 = boto3.client("s3", region_name=REGION)
lambda_client = boto3.client("lambda", region_name=REGION)


# =====================================================
# AWS TOOLS
# =====================================================

def list_ec2_instances():

    response = ec2.describe_instances()

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            instances.append({
                "InstanceId": instance["InstanceId"],
                "State": instance["State"]["Name"],
                "Type": instance["InstanceType"]
            })

    return instances


def list_s3_buckets():

    response = s3.list_buckets()

    return [b["Name"] for b in response["Buckets"]]


def list_lambda_functions():

    response = lambda_client.list_functions()

    return [
        f["FunctionName"]
        for f in response["Functions"]
    ]


# =====================================================
# TOOL EXECUTOR
# =====================================================

TOOLS = {
    "list_ec2_instances": list_ec2_instances,
    "list_s3_buckets": list_s3_buckets,
    "list_lambda_functions": list_lambda_functions,
}


# =====================================================
# NOVA CALL
# =====================================================

def invoke_nova(messages):

    body = {
        "messages": messages,
        "inferenceConfig": {
            "temperature": 0,
            "maxTokens": 800
        }
    }

    response = bedrock.invoke_model(
        modelId="amazon.nova-pro-v1:0",
        body=json.dumps(body)
    )

    result = json.loads(
        response["body"].read()
    )

    return result["output"]["message"]["content"][0]["text"]


# =====================================================
# AUTONOMOUS LOOP
# =====================================================

def autonomous_agent(goal):

    messages = []

    system_prompt = """
You are an autonomous AWS Cloud Agent.

Available tools

1. list_ec2_instances
2. list_s3_buckets
3. list_lambda_functions

Rules:

Think before acting.

Return ONLY valid JSON.

If you need a tool:

{
    "thought":"reasoning",
    "action":"tool_name"
}

If you have enough information:

{
    "thought":"done",
    "action":"finish",
    "answer":"complete answer"
}
"""

    messages.append({
        "role":"user",
        "content":[
            {
                "text":system_prompt +
                f"\n\nUser Goal:\n{goal}"
            }
        ]
    })

    while True:

        print("\n==============================")
        print("Thinking...")
        print("==============================")

        response = invoke_nova(messages)

        print(response)

        decision = json.loads(response)

        action = decision["action"]

        if action == "finish":

            print("\nFINAL ANSWER\n")
            print(decision["answer"])
            break

        print(f"\nExecuting Tool : {action}")

        observation = TOOLS[action]()

        print(observation)

        messages.append({
            "role":"assistant",
            "content":[
                {
                    "text":response
                }
            ]
        })

        messages.append({
            "role":"user",
            "content":[
                {
                    "text":
f"""
Tool Result

Tool:
{action}

Observation:

{json.dumps(observation,indent=2)}

Decide your next action.

Remember:

Return ONLY JSON.
"""
                }
            ]
        })


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    goal = input("Enter your goal : ")

    autonomous_agent(goal)