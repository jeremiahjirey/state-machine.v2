import json
import boto3
import os
import uuid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    try:
        body = event.get("data") or event

        item_id = body.get("id") or f"item-{uuid.uuid4().hex[:8]}"

        item = {
            "id": item_id,
            "name": body["name"],
            "stok": int(body["stok"]),
            "harga": int(body["harga"])
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Item added successfully",
                "item": item
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
