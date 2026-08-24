import boto3

ec2 = boto3.client("ec2")

response = ec2.describe_instances()

instances = []

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        instances.append({
            "id": instance["InstanceId"],
            "state": instance["State"]["Name"],
            "type": instance["InstanceType"]
        })

if not instances:
    print("No EC2 instances found.")
else:
    print("EC2 Instances:")

    for instance in instances:
        print(
            f"{instance['id']} → "
            f"{instance['state']} → "
            f"{instance['type']}"
        )