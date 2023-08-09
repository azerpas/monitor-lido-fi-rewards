import json
import boto3
import os
import urllib3
from lambda_config import get_latest_balance
import lido
from discord import post_to_discord

ADDRESS = os.environ.get("ADDRESS")
URL = f"https://stake.lido.fi/api/rewards?address={ADDRESS}&currency=usd&onlyRewards=false&archiveRate=true&skip=0&limit=7"
FUNCTION_NAME = os.environ.get("FUNCTION_NAME")

def lambda_handler(event, context):
    http = urllib3.PoolManager()

    client = boto3.client("lambda")
    config = client.get_function_configuration(
        FunctionName=FUNCTION_NAME,
    )

    previous_balance = get_latest_balance(config)

    response = http.request(
        "GET", URL, headers={"Content-Type": "application/json"}, retries=False
    )
    rewards = json.loads(response.data)

    rewards = lido.read_rewards(rewards)

    new_total_rewards_in_usd = rewards["in_usd_total"]
    new_total_rewards_in_eth = rewards["in_eth_total"]

    change_1w = (
        (rewards["balance"] - previous_balance)
        / (previous_balance if previous_balance != 0 else 1)
        * 100
    )

    post_to_discord(
        rewards["in_usd_weekly"],
        rewards["in_eth_weekly"],
        new_total_rewards_in_usd,
        new_total_rewards_in_eth,
        rewards["average_apr"],
        rewards["balance"],
        change_1w,
        ADDRESS,
    )

    client.update_function_configuration(
        FunctionName=FUNCTION_NAME,
        Environment={
            "Variables": {
                "LATEST_BALANCE": str(rewards["balance"]),
                "ADDRESS": os.environ.get("ADDRESS"),
                "WEBHOOK": os.environ.get("WEBHOOK"),
                "FUNCTION_NAME": os.environ.get("FUNCTION_NAME"),
            }
        },
    )

    return {"statusCode": 200, "body": json.dumps("Hello from Lambda!")}
