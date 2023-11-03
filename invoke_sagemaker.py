import json
import pprint

import boto3

# Reads ENDPOINT_NAME from cdk_output.json
with open("cdk_output.json", "r") as file:
    cdk_output = json.load(file)

ENDPOINT_NAME = cdk_output["ModelEndpointStack"]["EndpointName"]

payload = {
    "inputs": [
        [
            {
                "role": "system",
                "content": "DEFAULT_PROMPT",
            },
            {
                "role": "user",
                "content": "Write a hello world program in python3",
            },
        ]
    ],
    "parameters": {"max_new_tokens": 256, "top_p": 0.9, "temperature": 0.6},
}

runtime = boto3.client("runtime.sagemaker")


def invoke_llm(payload):
    response = runtime.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType="application/json",
        Body=json.dumps(payload),
        CustomAttributes="accept_eula=true",
    )

    result = json.loads(response["Body"].read().decode())

    return result


print("input")
pprint.pprint(payload["inputs"])
print("------")
print("output")
output = invoke_llm(payload=payload)
output_text = output[0]["generation"]["content"]
print(output_text)
