import boto3

cloudwatch = boto3.client("cloudwatch")

response = cloudwatch.describe_alarms()

alarms = response["MetricAlarms"]

if not alarms:
    print("No CloudWatch alarms found.")
else:
    print("CloudWatch Alarms:")

    for alarm in alarms:
        print(f"Alarm: {alarm['AlarmName']}")
        print(f"State: {alarm['StateValue']}")
        print(f"Description: {alarm.get('AlarmDescription', 'None')}")
        print("-------------------------")