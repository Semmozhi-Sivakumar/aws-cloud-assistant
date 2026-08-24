import boto3

iam = boto3.client("iam")

print("IAM SECURITY DATA:\n")

response = iam.list_users()

for user in response["Users"]:

    username = user["UserName"]

    print(f"User: {username}")

    attached = iam.list_attached_user_policies(
        UserName=username
    )

    print("Attached policies:")

    if attached["AttachedPolicies"]:

        for policy in attached["AttachedPolicies"]:
            print(f"  - {policy['PolicyName']}")

    else:
        print("  None")

    inline = iam.list_user_policies(
        UserName=username
    )

    print("Inline policies:")

    if inline["PolicyNames"]:

        for policy_name in inline["PolicyNames"]:
            print(f"  - {policy_name}")

    else:
        print("  None")

    print("-------------------------")