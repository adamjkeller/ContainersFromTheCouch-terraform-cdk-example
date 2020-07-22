#### Welcome 

This repo houses the code that was demoed on #ContainersFromTheCouch [here](https://youtu.be/9s_BAyQIAhs)

#### Prerequisites

Follow the [link](https://github.com/hashicorp/terraform-cdk/blob/master/docs/getting-started/python.md) and go through installing all the prerequisites prior to running the code.

Replace the subnet and security group values in the `main.py`. 

run `cdktf get` to pull down all the required modules.

#### Commands

cdktf synth <-- Generates the assembly TF code into the cdktf.out directory
cdktf diff <-- Executes a diff of proposed changes against current environment
cdkt deploy <-- Deploys the code