from typing import List, Dict


class Event:
    id: str
    total_pooled_ether_before: str
    total_pooled_ether_after: str
    total_shares_before: str
    total_shares_after: str
    apr: str
    block: int
    block_time: int
    log_index: int
    type: str
    report_shares: str
    balance: str
    rewards: str
    change: str
    currency_change: str
    epoch_days: str
    epoch_full_days: int

    def __init__(self, id: str, total_pooled_ether_before: str, total_pooled_ether_after: str, total_shares_before: str, total_shares_after: str, apr: str, block: int, block_time: int, log_index: int, type: str, report_shares: str, balance: str, rewards: str, change: str, currency_change: str, epoch_days: str, epoch_full_days: int) -> None:
        self.id = id
        self.total_pooled_ether_before = total_pooled_ether_before
        self.total_pooled_ether_after = total_pooled_ether_after
        self.total_shares_before = total_shares_before
        self.total_shares_after = total_shares_after
        self.apr = apr
        self.block = block
        self.block_time = block_time
        self.log_index = log_index
        self.type = type
        self.report_shares = report_shares
        self.balance = balance
        self.rewards = rewards
        self.change = change
        self.currency_change = currency_change
        self.epoch_days = epoch_days
        self.epoch_full_days = epoch_full_days


class Totals:
    eth_rewards: str
    currency_rewards: str

    def __init__(self, eth_rewards: str, currency_rewards: str) -> None:
        self.eth_rewards = eth_rewards
        self.currency_rewards = currency_rewards


class Rewards:
    events: List[Event]
    totals: Totals
    average_apr: str
    eth_to_st_eth_ratio: float
    st_eth_currency_price: Dict[str, float]
    total_items: int

    def __init__(self, events: List[Event], totals: Totals, average_apr: str, eth_to_st_eth_ratio: float, st_eth_currency_price: Dict[str, float], total_items: int) -> None:
        self.events = events
        self.totals = totals
        self.average_apr = average_apr
        self.eth_to_st_eth_ratio = eth_to_st_eth_ratio
        self.st_eth_currency_price = st_eth_currency_price
        self.total_items = total_items
