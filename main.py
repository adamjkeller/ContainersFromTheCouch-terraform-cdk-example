#!/usr/bin/env python

from constructs import Construct
from cdktf import App, TerraformStack
from imports.aws import AwsProvider, EcsCluster, EcsTaskDefinition, EcsService, EcsServiceNetworkConfiguration


class NginxECSService(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # Defining my provider 
        AwsProvider(self, "AWS", region="us-west-2")
        
        # Creating the ECS Cluster
        ecs_cluster = EcsCluster(
            self, "CftC",
            name="ContainersFromTheCouchLive"
        )
        
        # Creating a task definition for the nginx service
        task_definition = EcsTaskDefinition(
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
            family="cfclatest",
            requires_compatibilities=["FARGATE"],
            network_mode="awsvpc",
            cpu="512",
            memory="2048"
        )
        
        # Creating an ECS service
        EcsService(
            self, "NginxService",
            cluster=ecs_cluster.id,
            name="nginx-service-latest",
            desired_count=1,
            task_definition=task_definition.arn,
            network_configuration=[
                EcsServiceNetworkConfiguration(
                    subnets=['<REPLACE>', '<REPLACE>'],
                    assign_public_ip=True,
                    security_groups=['<REPLACE>']
                )
            ],
            launch_type="FARGATE"
        )


app = App()
NginxECSService(app, "containersfromthecouch")

app.synth()