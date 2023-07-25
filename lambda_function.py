import json
import boto3
import os
import urllib3
from lambda_config import get_latest_balance, get_total_rewards_in_eth, get_total_rewards_in_usd
import lido
from discord import post_to_discord

ADDRESS = os.environ.get('ADDRESS')
URL = f'https://stake.lido.fi/api/rewards?address={ADDRESS}&currency=usd&onlyRewards=false&archiveRate=true&skip=0&limit=7'
FUNCTION_NAME = os.environ.get('FUNCTION_NAME')

def lambda_handler(event, context):
    http = urllib3.PoolManager()

    client = boto3.client('lambda')
    config = client.get_function_configuration(
        FunctionName=FUNCTION_NAME,
    )
    
    total_rewards_in_eth = get_total_rewards_in_eth(config)
    total_rewards_in_usd = get_total_rewards_in_usd(config)
    latest_balance = get_latest_balance(config)
    
    response = http.request('GET',
        URL,
        headers = {'Content-Type': 'application/json'},
        retries = False)
    rewards = json.loads(response.data)
    
    rewards = lido.read_rewards(rewards)
    
    new_total_rewards_in_usd = total_rewards_in_usd + rewards['in_usd']
    new_total_rewards_in_eth = total_rewards_in_usd + rewards['in_eth']

    change_1w = (rewards['balance'] - latest_balance) / latest_balance * 100
    
    post_to_discord(rewards['in_usd'], rewards['in_eth'], new_total_rewards_in_usd, new_total_rewards_in_eth, rewards['average_apr'], rewards['balance'], change_1w, ADDRESS)
    
    client.update_function_configuration(
        FunctionName=FUNCTION_NAME,
        Environment={
            'Variables': {
                'LATEST_BALANCE': str(rewards['balance']),
                'TOTAL_REWARDS_IN_USD': str(new_total_rewards_in_usd),
                'TOTAL_REWARDS_IN_ETH': str(new_total_rewards_in_eth),
                'ADDRESS': os.environ.get('ADDRESS'),
                'WEBHOOK': os.environ.get('WEBHOOK'),
                'FUNCTION_NAME': os.environ.get('FUNCTION_NAME')
            }
        }
    )
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


