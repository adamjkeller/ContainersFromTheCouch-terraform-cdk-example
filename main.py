#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from imports.aws import Instance, AwsProvider, Vpc, EcsCluster, EcsTaskDefinition, EcsService, EcsServiceNetworkConfiguration


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # Defining my provider
        AwsProvider(self, 'Aws', region='us-west-2')
        
        # Easy, build an EC2 instance
        #Instance(self, "hello", ami="ami-a0cfeed8", instance_type="t2.micro")
        
        # Build an ECS Cluster
        ecs_cluster = EcsCluster(self, "ContainersFromTheCouch", name='ContainersFromTheCouch')
        
        # Build an ECS Task Definition
        nginx_task_def = EcsTaskDefinition(
            self, "TaskDef",
            container_definitions="""[
              {
                "name": "nginx",
                "image": "nginx:latest",
                "essential": true,
                "portMappings": [
                  {
                    "containerPort": 80,
                    "hostPort": 80
                  }
                ]
              }
            ]""",
            family="cfc",
            requires_compatibilities=["FARGATE"],
            network_mode="awsvpc",
            cpu="512",
            memory="2048"
        )
        
        EcsService(
            self, "NginxService",
            cluster=ecs_cluster.id,
            name="nginx-service",
            desired_count=1,
            task_definition=nginx_task_def.arn,
            network_configuration=[
                EcsServiceNetworkConfiguration(
                    subnets=['subnet-891ad8f1', 'subnet-b17aa7ec'],
                    assign_public_ip=True,
                    security_groups=['sg-0b52a3487bce05901']
                )
            ],
            launch_type="FARGATE"
        )


app = App()
MyStack(app, "terraform-cdk-tests")

app.synth()