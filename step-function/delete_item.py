import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    try:
        body = event.get("data") or event
        item_id = body.get("id")

        if not item_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'id' in request"})
            }

        # Optional: check if item exists
        existing = table.get_item(Key={"id": item_id})
        if "Item" not in existing:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Item not found"})
            }

        # Delete the item
        table.delete_item(Key={"id": item_id})

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Item with id '{item_id}' deleted successfully"
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
