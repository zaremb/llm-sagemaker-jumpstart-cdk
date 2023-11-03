#!/usr/bin/env python3

import aws_cdk as cdk

from model_endpoint_stack.model_endpoint_stack import ModelEndpointStack

# Llama models available as jumpstart:
# Llama-2-7b 	    meta-textgeneration-llama-2-7b 	    4096 	ml.g5.2xlarge
# Llama-2-7b-chat 	meta-textgeneration-llama-2-7b-f 	4096 	ml.g5.2xlarge
# Llama-2-13b 	    meta-textgeneration-llama-2-13b 	4096 	ml.g5.12xlarge
# Llama-2-13b-chat 	meta-textgeneration-llama-2-13b-f 	4096 	ml.g5.12xlarge
# Llama-2-70b 	    meta-textgeneration-llama-2-70b     4096 	ml.g5.48xlarge
# Llama-2-70b-chat 	meta-textgeneration-llama-2-70b-f 	4096 	ml.g5.48xlarge

app = cdk.App()

# Change this if you do not want to use defaults from cdk.json
model_package_name = app.node.get_context("default_model_package_name")
instance_type = app.node.get_context("default_instance_type")
instance_count = app.node.get_context("default_instance_count")
model_endpoint_stack = ModelEndpointStack(
    app,
    "ModelEndpointStack",
    model_package_name=model_package_name,
    instance_type=instance_type,
    instance_count=instance_count,
)


cdk.CfnOutput(
    scope=model_endpoint_stack,
    id="EndpointName",
    value=model_endpoint_stack.endpoint.attr_endpoint_name,
)
app.synth(force=True)
