import urllib3
import os
import json
from lido import wei_to_eth

def post_to_discord(rewards_in_usd: float, rewards_in_eth: float, total_rewards_in_usd: float, total_rewards_in_eth: float, average_apr, balance, change_1w, address):
    http = urllib3.PoolManager()

    # Set headers
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Python/urllib3'
    }

    # Construct the embed
    embed = {
        "title": "Lido Staking Rewards (1 week)",
        "fields": [
            {"name": "Rewards (USD)", "value": "{:.2f}$".format(rewards_in_usd)},
            {"name": "Rewards (ETH)", "value": str(wei_to_eth(rewards_in_eth))},
            {"name": "Total rewards (USD)", "value": "{:.2f}$".format(total_rewards_in_usd)},
            {"name": "Total rewards (ETH)", "value": str((wei_to_eth(total_rewards_in_eth)))},
            {"name": "Average APR", "value": str(average_apr) + "%"},
            {"name": "Balance (ETH)", "value": str(balance)},
            {"name": "Change", "value": str(change_1w) + "%"},
            {"name": "Etherscan Link", "value": f"http://etherscan.io/address/{address}"},
            {"name": "Stake Lido Link", "value": "https://stake.lido.fi/"},
        ]
    }

    # Perform POST request
    response = http.request(
        'POST',
        os.environ.get('WEBHOOK'),
        body=json.dumps({"content": f"You've earned {str(rewards_in_usd)}$ from Lido.fi this week! 🎉", "embeds": [embed]}),
        headers=headers
    )

    if response.status != 204:
        raise Exception(f"POST to Discord returned status {response.status}. Response: {response.data}")