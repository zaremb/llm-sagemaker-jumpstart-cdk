# LLM SageMaker Jumpstart CDK
Hello! This repository shows how to deploy sample CDK app that has live SageMaker endpoint with LLM (by default, Llama2-7b chat).
## Installation
- Install CDK
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
## Deployment
To deploy, run:
```
cdk deploy
```
If asked `Do you wish to deploy these changes` enter `y`

## Invoking
To invoke endpoint directly, run:
```
python3 invoke_sagemaker.py
```
The script will automatically read endpoint name from output of CDK

## Destroy
Run
```
cdk destroy
```
And when asked for approval, enter `y`
