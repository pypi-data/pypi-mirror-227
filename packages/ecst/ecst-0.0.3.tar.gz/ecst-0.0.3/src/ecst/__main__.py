import argparse
import boto3
import json
import subprocess

parser = argparse.ArgumentParser(
                    prog='ecs-tunnel',
                    description='Create local tunnels and sessions to AWS ECS services running in a VPC',)
parser.add_argument('cluster',
                    help='The name of the ECS cluster')
parser.add_argument('service',
                    help='The name of the ECS service')
parser.add_argument('--local-port', default=3001)
parser.add_argument('--remote-port', default=3000)
parser.add_argument('--region', default="eu-west-2")
parser.add_argument('--aws-profile', default="default")

args = parser.parse_args()

ecsClient = boto3.client('ecs')
ssmClient = boto3.client('ssm')

services_response = ecsClient.list_services(
  cluster=args.cluster
)

service_arn = [k for k in services_response['serviceArns'] if args.service in k][0]

tasks_response = ecsClient.list_tasks(
  cluster=args.cluster,
  serviceName=service_arn
)

task_arn = tasks_response['taskArns'][0]
task_id = task_arn.split('/')[-1]

tasks_response = ecsClient.describe_tasks(
  cluster=args.cluster,
  tasks=[task_arn]
)

container_id = tasks_response['tasks'][0]['containers'][0]['runtimeId']

target=f"ecs:%s_%s_%s" % (args.cluster, task_id, container_id)

ssm_response = ssmClient.start_session(
  Target=target,
  DocumentName="AWS-StartPortForwardingSession",
  Parameters={
    "portNumber": [
      str(args.remote_port),
    ],
    "localPortNumber": [
      str(args.local_port),
    ],
  }
)

cmd = [
    '/usr/local/sessionmanagerplugin/bin/session-manager-plugin',
    json.dumps(ssm_response),
    args.region,
    'StartSession',
    args.aws_profile,
    json.dumps(dict(Target=target)),
    f'https://ssm.%s.amazonaws.com' % (args.region)

]
subprocess.run(cmd)
