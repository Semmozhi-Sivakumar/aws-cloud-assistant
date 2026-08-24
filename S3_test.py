import boto3

s3 = boto3.client("s3")

response = s3.list_buckets()

buckets = response["Buckets"]

if not buckets:
    print("No S3 buckets found.")
else:
    print("S3 Buckets:")

    for bucket in buckets:
        print(f"Bucket: {bucket['Name']}")