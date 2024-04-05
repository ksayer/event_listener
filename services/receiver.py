from datetime import datetime
from typing import Protocol

from web3 import Web3
from web3.types import EventData

from database.models import TotalDistribution


class Receiver(Protocol):
    def save(self, event: EventData, w3: Web3) -> None:
        ...


class EventReceiver:
    def save(self, event: EventData, w3: Web3):
        event_args = event.get('args')
        block = w3.eth.get_block(event['blockNumber'])
        if event_args:
            TotalDistribution.create(
                aix_processed=event_args['inputAixAmount'],
                aix_distributed=event_args['distributedAixAmount'],
                eth_bought=event_args['swappedEthAmount'],
                eth_distributed=event_args['distributedEthAmount'],
                created=datetime.fromtimestamp(block['timestamp'])
            )
