import boto3

iam = boto3.client("iam")

response = iam.list_users()

users = response["Users"]

if not users:
    print("No IAM users found.")
else:
    print("IAM Users:")

    for user in users:
        print(f"User: {user['UserName']}")