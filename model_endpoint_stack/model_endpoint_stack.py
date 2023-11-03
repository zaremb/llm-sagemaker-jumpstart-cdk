from aws_cdk import Stack
from aws_cdk import aws_iam as iam
from aws_cdk import aws_sagemaker as sagemaker
from constructs import Construct


class ModelEndpointStack(Stack):
    PRIMARY_VARIANT_NAME = "AllTraffic"
    VARIANT_WEIGHT = 1

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        model_package_name,
        instance_type,
        instance_count,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.execution_role = iam.Role(
            self,
            "sm-execution-role",
            assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"),
        )
        self.execution_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess")
        )  # TODO: Narrow down
        self.execution_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess")
        )  # TODO: Narrow down

        self.model = sagemaker.CfnModel(
            self,
            "model",
            execution_role_arn=self.execution_role.role_arn,
            containers=[
                sagemaker.CfnModel.ContainerDefinitionProperty(
                    model_package_name=model_package_name,  # Note: model package name and model package arn are the same thing
                )
            ],
            enable_network_isolation=True,
        )

        self.endpoint_config = sagemaker.CfnEndpointConfig(
            self,
            "endpoint-config",
            production_variants=[
                sagemaker.CfnEndpointConfig.ProductionVariantProperty(
                    model_name=self.model.attr_model_name,
                    variant_name=__class__.PRIMARY_VARIANT_NAME,
                    instance_type=instance_type,
                    initial_instance_count=instance_count,
                    initial_variant_weight=__class__.VARIANT_WEIGHT,
                )
            ],
        )

        self.endpoint = sagemaker.CfnEndpoint(
            self,
            "endpoint",
            endpoint_config_name=self.endpoint_config.attr_endpoint_config_name,
        )
