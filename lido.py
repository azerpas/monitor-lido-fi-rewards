from lido_types import Rewards

def wei_to_eth(wei):
    return wei / (10**18)

def read_rewards(rewards: Rewards):
    if 'events' in rewards:
        latest_event = rewards['events'][0] if rewards['events'] else None

        if latest_event:
            balance = float(latest_event['balance'])
    
    rewards_totals = rewards['totals']
    
    if 'averageApr' in rewards:
        average_apr = float(rewards['averageApr'])
    else:
        average_apr = 0.0
        
    if 'ethRewards' in rewards_totals:
        rewards_in_eth = float(rewards_totals['ethRewards'])
    else:
        rewards_in_eth = 0.0
        
    if 'currencyRewards' in rewards_totals:
        rewards_in_usd = float(rewards_totals['currencyRewards'])
    else:
        rewards_in_usd = 0.0
    
    usd_weekly_rewards = 0
    eth_weekly_rewards = 0
    for event in rewards['events']:
        usd_weekly_rewards += float(event['currencyChange'])
        eth_weekly_rewards += float(event['change'])

    return {
        "in_usd_weekly": usd_weekly_rewards if usd_weekly_rewards else 0.0,
        "in_eth_weekly": eth_weekly_rewards if eth_weekly_rewards else 0.0,
        "in_usd_total": rewards_in_usd if rewards_in_usd else 0.0,
        "in_eth_total": rewards_in_eth if rewards_in_eth else 0.0,
        "average_apr": average_apr if average_apr else 0.0,
        "balance": balance if balance else 0.0
    }