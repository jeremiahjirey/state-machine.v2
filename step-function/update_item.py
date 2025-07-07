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

        update_fields = {}
        expression = []
        values = {}
        attr_names = {}

        if "name" in body:
            update_fields["#n"] = "name"
            expression.append("#n = :name")
            values[":name"] = body["name"]
            attr_names["#n"] = "name"

        if "stok" in body:
            expression.append("stok = :stok")
            values[":stok"] = int(body["stok"])

        if "harga" in body:
            expression.append("harga = :harga")
            values[":harga"] = int(body["harga"])

        if not expression:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No fields to update"})
            }

        update_expression = "SET " + ", ".join(expression)

        kwargs = {
            "Key": {"id": item_id},
            "UpdateExpression": update_expression,
            "ExpressionAttributeValues": values
        }

        if attr_names:
            kwargs["ExpressionAttributeNames"] = attr_names

        table.update_item(**kwargs)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Item updated successfully",
                "updated_fields": list(values.keys())
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
