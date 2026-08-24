import os
import boto3

from dotenv import load_dotenv
from openai import OpenAI


# -------------------------
# NVIDIA SETUP
# -------------------------

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)


# -------------------------
# AWS SETUP
# -------------------------

ec2 = boto3.client("ec2")
s3 = boto3.client("s3")
iam = boto3.client("iam")
cloudwatch = boto3.client("cloudwatch")


# -------------------------
# GET EC2 INFORMATION
# -------------------------

def get_ec2_data():

    response = ec2.describe_instances()

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:

            instance_info = {
                "id": instance["InstanceId"],
                "state": instance["State"]["Name"],
                "type": instance["InstanceType"],
                "availability_zone": instance["Placement"]["AvailabilityZone"],
                "private_ip": instance.get("PrivateIpAddress", "None"),
                "public_ip": instance.get("PublicIpAddress", "None")
            }

            instances.append(instance_info)

    if not instances:
        return "There are currently no EC2 instances."

    aws_data = "EC2 Instances:\n"

    for instance in instances:
        aws_data += (
            f"Instance ID: {instance['id']}\n"
            f"State: {instance['state']}\n"
            f"Type: {instance['type']}\n"
            f"Availability Zone: {instance['availability_zone']}\n"
            f"Private IP: {instance['private_ip']}\n"
            f"Public IP: {instance['public_ip']}\n"
            f"-------------------------\n"
        )

    return aws_data

# -------------------------
# GET S3 INFORMATION
# -------------------------

def get_s3_data():

    s3_response = s3.list_buckets()

    buckets = s3_response["Buckets"]

    if not buckets:
        return "There are currently no S3 buckets."

    s3_data = "S3 Buckets:\n"

    for bucket in buckets:

        bucket_name = bucket["Name"]

        s3_data += f"\nBucket: {bucket_name}\n"

        try:
            objects_response = s3.list_objects_v2(
                Bucket=bucket_name
            )

            objects = objects_response.get("Contents", [])

            if not objects:
                s3_data += "Objects: 0\n"

            else:
                s3_data += f"Objects: {len(objects)}\n"

                total_size = 0

                for obj in objects:
                    total_size += obj["Size"]

                s3_data += f"Total size: {total_size} bytes\n"

        except Exception as e:
            s3_data += f"Could not read bucket contents: {e}\n"

    return s3_data

# -------------------------
# GET IAM INFORMATION
# -------------------------
def get_iam_data():

    response = iam.list_users()

    users = response["Users"]

    if not users:
        return "There are currently no IAM users."

    iam_data = "IAM Users:\n"

    for user in users:
        iam_data += f"User: {user['UserName']}\n"

    return iam_data
# ---------------------------
# GET IAM SECURITY DATA
# ---------------------------
def get_iam_security_data():

    response = iam.list_users()

    users = response["Users"]

    if not users:
        return "No IAM users found."

    iam_security_data = "IAM SECURITY INFORMATION:\n"

    for user in users:

        username = user["UserName"]

        iam_security_data += f"\nUser: {username}\n"

        # Managed policies
        attached = iam.list_attached_user_policies(
            UserName=username
        )

        if attached["AttachedPolicies"]:

            iam_security_data += "Attached policies:\n"

            for policy in attached["AttachedPolicies"]:

                iam_security_data += (
                    f"- {policy['PolicyName']}\n"
                )

        else:

            iam_security_data += (
                "Attached policies: None\n"
            )

        # Inline policies
        inline = iam.list_user_policies(
            UserName=username
        )

        if inline["PolicyNames"]:

            iam_security_data += "Inline policies:\n"

            for policy_name in inline["PolicyNames"]:

                iam_security_data += (
                    f"- {policy_name}\n"
                )

        else:

            iam_security_data += (
                "Inline policies: None\n"
            )

        iam_security_data += "-------------------------\n"

    return iam_security_data
# ---------------------------
# GET CLOUDWATCH INFORMATION
# ---------------------------
def get_cloudwatch_data():

    response = cloudwatch.describe_alarms()

    alarms = response["MetricAlarms"]

    if not alarms:
        return "No CloudWatch alarms found."

    cloudwatch_data = "CloudWatch Alarms:\n"

    for alarm in alarms:

        cloudwatch_data += (
            f"Alarm: {alarm['AlarmName']}\n"
            f"State: {alarm['StateValue']}\n"
            f"Description: "
            f"{alarm.get('AlarmDescription', 'None')}\n"
            f"-------------------------\n"
        )

    return cloudwatch_data

# -------------------------
# ASK USER
# -------------------------

user_question = input("\nAsk your AWS question: ")

# -------------------------
# AI SERVICE ROUTER
# -------------------------
router_response = client.chat.completions.create(

    model="nvidia/nemotron-3.5-lightning-30b-a3b",

    messages=[

        {
            "role": "system",

            "content": """
You are ONLY an AWS service classification system.

You MUST return exactly ONE of these words:

EC2
S3
IAM
MULTI
HEALTH
CLOUDWATCH
SECURITY
UNKNOWN

Rules:

EC2 = question about EC2 instances or compute.

S3 = question about S3 buckets or objects.

IAM = question about IAM users, roles, policies,
or permissions.

MULTI = question asking for an overview or
information from multiple AWS services.

HEALTH = question asking about the health,
problems, risks, issues, or overall condition
of the AWS environment.

CLOUDWATCH = questions about CloudWatch alarms or monitoring.

SECURITY = questions about IAM permissions, policies,
access levels, excessive permissions, or security concerns.

UNKNOWN = anything else.

IMPORTANT:

Return ONLY ONE WORD from the list above.

Do NOT explain.

Do NOT write a sentence.

Do NOT use punctuation.
"""
        },

        {
            "role": "user",

            "content": user_question
        }
    ],

    temperature=0
)
# =========================================================
# 9. CLEAN AND VALIDATE ROUTER RESULT
# =========================================================

service = (
    router_response
    .choices[0]
    .message
    .content
    .strip()
    .upper()
)


valid_services = {
    "EC2",
    "S3",
    "IAM",
    "CLOUDWATCH",
    "MULTI",
    "HEALTH",
    "SECURITY",
    "UNKNOWN"
}


# If AI gives an unexpected answer
if service not in valid_services:

    service = "UNKNOWN"


print("\nAI ROUTER:")
print(service)


# -------------------------
# CALL AWS SERVICE
# -------------------------
if service == "EC2":

    aws_data = get_ec2_data()

elif service == "S3":

    aws_data = get_s3_data()

elif service == "IAM":

    aws_data = get_iam_data()

elif service == "MULTI":

    ec2_data = get_ec2_data()
    s3_data = get_s3_data()
    iam_data = get_iam_data()

    aws_data = f"""
EC2 INFORMATION:
{ec2_data}

S3 INFORMATION:
{s3_data}

IAM INFORMATION:
{iam_data}
"""
elif service == "HEALTH":

    ec2_data = get_ec2_data()

    s3_data = get_s3_data()

    iam_data = get_iam_data()

    cloudwatch_data = get_cloudwatch_data()

    aws_data = f"""
EC2 INFORMATION:

{ec2_data}


S3 INFORMATION:

{s3_data}


IAM INFORMATION:

{iam_data}


CLOUDWATCH INFORMATION:

{cloudwatch_data}
"""
elif service == "CLOUDWATCH":

    aws_data = get_cloudwatch_data()   

elif service == "SECURITY":

    iam_security_data = get_iam_security_data()

    aws_data = f"""
IAM SECURITY INFORMATION:

{iam_security_data}
"""

else:

    aws_data = (
        "The question does not appear to require "
        "EC2, S3, or IAM information."
    )


# -------------------------
# SEND AWS DATA + QUESTION TO NEMOTRON
# -------------------------

response = client.chat.completions.create(
    model="nvidia/nemotron-3.5-lightning-30b-a3b",

    messages=[
        {
            
            "role": "system",
            "content": """
You are an AWS Cloud Assistant.

Answer the user's question using ONLY the AWS
information provided to you.

Never invent AWS resources, configurations,
security problems, or health issues.

Clearly distinguish between:

1. Confirmed facts from the AWS data.
2. Potential areas that should be checked.

If the AWS information is insufficient to make
a conclusion, clearly say that additional AWS
data is required.

For HEALTH questions:

Analyze the provided EC2, S3, IAM, and CloudWatch information.

Use CloudWatch alarm information as monitoring evidence.

If no CloudWatch alarms are found, state that as a
confirmed fact.

Do not interpret the absence of CloudWatch alarms as
proof that the entire AWS environment is healthy.

Identify reasonable areas that may need attention.

Clearly separate confirmed facts from areas that
require additional AWS data.

For SECURITY questions:

Analyze the provided IAM security information.

Identify permissions that may deserve review.

Do not automatically classify a permission as a
security vulnerability.

Explain why a permission may be broader than necessary.

Clearly distinguish confirmed permissions from
potential security concerns.

Do not invent IAM policies or permissions that were
not provided.

Do NOT invent CloudWatch metrics, AWS Health
Dashboard events, Trusted Advisor findings,
IAM policies, S3 permissions, or other data
that was not provided.
"""

        },

        {
            "role": "user",
            "content": f"""
AWS INFORMATION:

{aws_data}

USER QUESTION:

{user_question}
"""
        }
    ]
)

answer = response.choices[0].message.content

print("\nCLOUD ASSISTANT:")
print(answer)

