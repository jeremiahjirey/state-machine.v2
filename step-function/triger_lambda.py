import json
import boto3
import os

# Inisialisasi client Step Functions
sfn_client = boto3.client("stepfunctions")

# ARN State Machine dari environment variable
STATE_MACHINE_ARN = os.environ["STATE_MACHINE_ARN"]

def lambda_handler(event, context):
    try:
        # Ambil input dari API Gateway
        input_payload = event["body"]
        if isinstance(input_payload, str):
            input_payload = json.loads(input_payload)

        # Jalankan Step Function
        response = sfn_client.start_execution(
            stateMachineArn=STATE_MACHINE_ARN,
            input=json.dumps(input_payload)  # harus string JSON
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Step Function started",
                "executionArn": response["executionArn"]
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }
