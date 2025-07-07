import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    try:
        item_id = event.get("id") or (event.get("data") or {}).get("id")
        
        if not item_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'id' in request"})
            }

        response = table.get_item(Key={"id": item_id})

        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Item not found"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({"item": response["Item"]}, default=str)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
