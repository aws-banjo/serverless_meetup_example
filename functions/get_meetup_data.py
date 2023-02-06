import boto3
import os
import json

# define environment variables
TABLE_NAME = os.environ["TABLE_NAME"]

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def handler(event, context):
    print("Getting data")

    event_data = event["body"]
    meetup_id = json.loads(event_data)["meetup_id"]

    # Use the DynamoDB Table resource get item method to get a single item
    response = table.get_item(
        Key={
            "id": meetup_id,
        }
    )

    meetup_data = response["Item"]
    print(meetup_data)

    return meetup_data