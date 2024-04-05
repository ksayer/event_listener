from eth_typing import ChecksumAddress
from web3 import Web3

from core.settings import settings


def get_eth_balance(address: ChecksumAddress):
    w3 = Web3(Web3.HTTPProvider(settings.eth_rpc))
    return w3.eth.get_balance(address)
