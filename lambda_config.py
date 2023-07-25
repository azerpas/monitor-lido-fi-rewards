def get_total_rewards_in_eth(config):
    if 'TOTAL_REWARDS_IN_ETH' in config['Environment']['Variables']:
        return float(config['Environment']['Variables']['TOTAL_REWARDS_IN_ETH'])
    else:
        return 0
        
def get_total_rewards_in_usd(config):
    if 'TOTAL_REWARDS_IN_USD' in config['Environment']['Variables']:
        return float(config['Environment']['Variables']['TOTAL_REWARDS_IN_USD'])
    else:
        return 0
        
def get_latest_balance(config):
    if 'LATEST_BALANCE' in config['Environment']['Variables']:
        return float(config['Environment']['Variables']['LATEST_BALANCE'])
    else:
        return 0