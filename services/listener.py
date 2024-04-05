from dataclasses import dataclass

from eth_typing import ChecksumAddress
from web3 import Web3

from database.models import EventDaemon
from services.receiver import Receiver


@dataclass
class MonitoredEvent:
    contract_address: ChecksumAddress
    abi: list
    event_name: str
    receiver: Receiver


class EventListener:
    def __init__(
        self,
        rpc: str,
        monitored_event: MonitoredEvent,
    ):
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        self.monitored_event = monitored_event
        self.contract = self.w3.eth.contract(
            address=monitored_event.contract_address, abi=monitored_event.abi
        )

    def run(self):
        from_block, to_block = self._get_range_block()
        events = getattr(self.contract.events, self.monitored_event.event_name) \
                  .get_logs(fromBlock=from_block, toBlock=to_block)
        for event in events:
            self.monitored_event.receiver.save(event, self.w3)
        EventDaemon.update_block(to_block)

    def _get_range_block(self) -> tuple[int, int]:
        current_block = self.w3.eth.block_number
        daemon = EventDaemon.get_or_create(current_block)
        start_block = daemon.last_checked_block + 1
        return start_block, current_block
