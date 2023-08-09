def get_latest_balance(config):
    if 'LATEST_BALANCE' in config['Environment']['Variables']:
        return float(config['Environment']['Variables']['LATEST_BALANCE'])
    else:
        return 0