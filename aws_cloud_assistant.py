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
# ----------------------------
# GET S3 SECURITY INFORMATION 
# ----------------------------
def get_s3_security_data():

    s3 = boto3.client("s3")

    response = s3.list_buckets()

    buckets = response.get("Buckets", [])

    if not buckets:
        return "No S3 buckets found."

    security_data = "S3 SECURITY INFORMATION:\n"

    for bucket in buckets:

        bucket_name = bucket["Name"]

        security_data += f"\nBucket: {bucket_name}\n"

        # -------------------------
        # PUBLIC ACCESS BLOCK
        # -------------------------

        try:

            public_access = s3.get_public_access_block(
                Bucket=bucket_name
            )

            config = public_access[
                "PublicAccessBlockConfiguration"
            ]

            security_data += f"""
Public Access Block:
- BlockPublicAcls: {config.get("BlockPublicAcls")}
- IgnorePublicAcls: {config.get("IgnorePublicAcls")}
- BlockPublicPolicy: {config.get("BlockPublicPolicy")}
- RestrictPublicBuckets: {config.get("RestrictPublicBuckets")}
"""

        except Exception as e:

            security_data += (
                f"Public Access Block: Unable to retrieve ({e})\n"
            )

        # -------------------------
        # ENCRYPTION
        # -------------------------

        try:

            encryption = s3.get_bucket_encryption(
                Bucket=bucket_name
            )

            rules = encryption[
                "ServerSideEncryptionConfiguration"
            ]["Rules"]

            security_data += "Encryption:\n"

            for rule in rules:

                default_encryption = rule.get(
                    "ApplyServerSideEncryptionByDefault",
                    {}
                )

                algorithm = default_encryption.get(
                    "SSEAlgorithm"
                )

                security_data += (
                    f"- Algorithm: {algorithm}\n"
                )

        except s3.exceptions.ClientError:

            security_data += (
                "Encryption: No default bucket encryption configuration found.\n"
            )

        # -------------------------
        # VERSIONING
        # -------------------------

        try:

            versioning = s3.get_bucket_versioning(
                Bucket=bucket_name
            )

            status = versioning.get(
                "Status",
                "Disabled"
            )

            security_data += (
                f"Versioning: {status}\n"
            )

        except Exception as e:

            security_data += (
                f"Versioning: Unable to retrieve ({e})\n"
            )

        security_data += "\n-------------------------\n"

    return security_data
# ------------------------
# S3 ACCESS POLICY 
# ------------------------
def get_s3_access_policy_data():

    s3 = boto3.client("s3")

    response = s3.list_buckets()

    buckets = response.get("Buckets", [])

    if not buckets:
        return "No S3 buckets found."

    access_data = "S3 ACCESS CONTROL INFORMATION:\n"

    for bucket in buckets:

        bucket_name = bucket["Name"]

        access_data += f"\nBucket: {bucket_name}\n"

        # -------------------------
        # BUCKET POLICY
        # -------------------------

        try:

            policy_response = s3.get_bucket_policy(
                Bucket=bucket_name
            )

            policy = policy_response["Policy"]

            access_data += f"""
Bucket Policy:
{policy}
"""

        except s3.exceptions.ClientError as e:

            error_code = e.response["Error"]["Code"]

            if error_code == "NoSuchBucketPolicy":
                access_data += "Bucket Policy: None configured.\n"
            else:
                access_data += (
                    f"Bucket Policy: Unable to retrieve ({error_code})\n"
                )

        # -------------------------
        # BUCKET ACL
        # -------------------------

        try:

            acl_response = s3.get_bucket_acl(
                Bucket=bucket_name
            )

            access_data += "\nBucket ACL:\n"

            for grant in acl_response.get("Grants", []):

                grantee = grant.get("Grantee", {})
                permission = grant.get("Permission")

                grantee_type = grantee.get("Type")
                grantee_uri = grantee.get("URI")
                grantee_display_name = grantee.get(
                    "DisplayName"
                )

                access_data += (
                    f"- Type: {grantee_type}, "
                    f"Permission: {permission}, "
                    f"URI: {grantee_uri}, "
                    f"DisplayName: {grantee_display_name}\n"
                )

        except Exception as e:

            access_data += (
                f"Bucket ACL: Unable to retrieve ({e})\n"
            )

        access_data += "\n-------------------------\n"

    return access_data

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
#  IAM POLICY DOCUMENTS.
# ---------------------------
def get_iam_policy_documents():

    response = iam.list_users()

    users = response["Users"]

    if not users:
        return "No IAM users found."

    policy_data = "IAM POLICY DOCUMENTS:\n"

    for user in users:

        username = user["UserName"]

        policy_data += f"\nUSER: {username}\n"

        # -------------------------
        # MANAGED POLICIES
        # -------------------------

        attached = iam.list_attached_user_policies(
            UserName=username
        )

        for policy in attached["AttachedPolicies"]:

            policy_name = policy["PolicyName"]
            policy_arn = policy["PolicyArn"]

            policy_info = iam.get_policy(
                PolicyArn=policy_arn
            )

            default_version = policy_info["Policy"]["DefaultVersionId"]

            version = iam.get_policy_version(
                PolicyArn=policy_arn,
                VersionId=default_version
            )

            document = version["PolicyVersion"]["Document"]

            policy_data += f"""
Managed Policy: {policy_name}
Policy ARN: {policy_arn}
Policy Document:
{document}
"""

        # -------------------------
        # INLINE POLICIES
        # -------------------------

        inline = iam.list_user_policies(
            UserName=username
        )

        for policy_name in inline["PolicyNames"]:

            inline_policy = iam.get_user_policy(
                UserName=username,
                PolicyName=policy_name
            )

            document = inline_policy["PolicyDocument"]

            policy_data += f"""
Inline Policy: {policy_name}
Policy Document:
{document}
"""

        policy_data += "\n-------------------------\n"

    return policy_data
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

def get_cloudwatch_health_data():

    cloudwatch = boto3.client("cloudwatch")

    response = cloudwatch.describe_alarms()

    alarms = response.get("MetricAlarms", [])

    if not alarms:
        return "No CloudWatch metric alarms found."

    health_data = "CLOUDWATCH HEALTH INFORMATION:\n"

    for alarm in alarms:

        health_data += f"""
Alarm Name: {alarm.get("AlarmName")}
State: {alarm.get("StateValue")}
State Reason: {alarm.get("StateReason")}
Metric: {alarm.get("MetricName")}
Namespace: {alarm.get("Namespace")}
Statistic: {alarm.get("Statistic")}
Threshold: {alarm.get("Threshold")}
Comparison: {alarm.get("ComparisonOperator")}
"""

        health_data += "\n-------------------------\n"

    return health_data

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
You are an AWS question router.

Classify the user's question into exactly ONE of these categories:

EC2
S3
IAM
CLOUDWATCH
SECURITY
S3_SECURITY
HEALTH
MULTI
UNKNOWN

Rules:

EC2:
Questions about EC2 instances, instance IDs, instance state,
instance type, IP addresses, availability zones, or compute resources.

S3:
Questions about S3 buckets, objects, object counts, bucket size,
or S3 resources.

IAM:
Questions about IAM users, IAM roles, IAM groups, or basic IAM information.

CLOUDWATCH:
Questions about CloudWatch alarms, metrics, or monitoring information.

SECURITY:
Questions about IAM security, permissions, attached policies,
inline policies, policy documents, excessive permissions,
least privilege, or security concerns.

HEALTH:
Questions asking whether the AWS environment is healthy,
safe, or operating normally.

S3_SECURITY:
Questions about S3 bucket security, public access,
encryption, versioning, bucket security configuration,
or whether an S3 bucket is securely configured.

Examples:
"Is my S3 bucket secure?"
"Is my S3 bucket public?"
"Is encryption enabled on my S3 bucket?"
"Is S3 versioning enabled?"
"Are there any S3 security concerns?"

Classify these questions as S3_SECURITY.

MULTI:
Questions requiring information from multiple AWS services.

UNKNOWN:
Questions that do not relate to the available AWS services.

Important:
If the user asks something like:
"Are there any IAM security concerns?"
"Is my IAM secure?"
"Do I have excessive IAM permissions?"
"Which users have broad permissions?"
"Are any IAM policies too permissive?"

classify the question as:

SECURITY

Return ONLY the category name.
Do not explain your answer.
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
    "S3_SECURITY",
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

    s3_security_data = get_s3_security_data()

    s3_access_data = get_s3_access_policy_data()

    iam_data = get_iam_security_data()

    iam_policy_data = get_iam_policy_documents()

    cloudwatch_data = get_cloudwatch_health_data()

    aws_data = f"""
EC2 INFORMATION:

{ec2_data}

S3 INFORMATION:

{s3_data}

S3 SECURITY INFORMATION:

{s3_security_data}

S3 ACCESS CONTROL INFORMATION:

{s3_access_data}

IAM SECURITY INFORMATION:

{iam_data}

IAM POLICY DOCUMENTS:

{iam_policy_data}

CLOUDWATCH HEALTH INFORMATION:

{cloudwatch_data}
"""
elif service == "CLOUDWATCH":

    aws_data = get_cloudwatch_data()   

elif service == "SECURITY":

    iam_security_data = get_iam_security_data()

    iam_policy_documents = get_iam_policy_documents()

    aws_data = f"""
IAM SECURITY INFORMATION:

{iam_security_data}

IAM POLICY DOCUMENTS:

{iam_policy_documents}
"""
elif service == "S3_SECURITY":

    s3_security_data = get_s3_security_data()

    s3_access_data = get_s3_access_policy_data()

    aws_data = f"""
S3 SECURITY INFORMATION:

{s3_security_data}

S3 ACCESS CONTROL INFORMATION:

{s3_access_data}
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

Assess the AWS environment ONLY using the AWS data provided.

Consider:

- EC2 information
- S3 information
- IAM information
- CloudWatch information

Clearly separate:

1. Confirmed healthy/normal observations
2. Potential concerns
3. Missing monitoring or configuration data

Important:

"No CloudWatch alarms found" does NOT mean the AWS
environment is healthy.

Do not claim the environment is healthy unless the
provided data supports that conclusion.

Do not invent AWS resources, metrics, alarms,
configurations, or health events.

If the provided data is insufficient for a complete
health assessment, clearly state what additional data
would be required.

For SECURITY questions:

Analyze the provided IAM users, attached policies,
inline policies, and actual IAM policy documents.

Identify permissions that may be broader than necessary.

Pay particular attention to:

- Full administrative permissions
- Wildcard actions such as "*"
- Wildcard resources such as "*"
- Permissions that allow modifying or deleting resources
- Differences between read-only and write permissions
- Permissions that may violate least-privilege principles

Do not automatically classify a broad permission as
a security vulnerability.

Explain why a permission may deserve review.

Clearly distinguish:

1. Confirmed permissions from the policy documents.
2. Potential security concerns.
3. Information that is still missing.

Do not invent permissions that are not present in
the provided policy documents.

Do not recommend changing or deleting permissions
without explaining the reason and potential impact.

For S3_SECURITY questions:

Analyze:

- Public Access Block settings
- Server-side encryption
- Versioning
- Bucket policies
- Bucket ACLs

Pay particular attention to:

- Principal "*"
- Allow statements
- s3:GetObject
- s3:PutObject
- s3:DeleteObject
- s3:*
- Public or cross-account access

Clearly distinguish confirmed access permissions
from potential security concerns.

If a bucket policy contains:
Principal: "*"
with:
Effect: Allow
and an object-access action such as s3:GetObject,

identify this as confirmed public access unless
the provided AWS data shows a restriction that prevents it.

Do not claim that a bucket is completely insecure
based on one finding alone.

Do not invent missing bucket policies, ACLs,
encryption settings, or permissions.

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

