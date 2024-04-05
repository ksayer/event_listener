import json

from web3 import Web3

from core.settings import settings
from services.listener import MonitoredEvent, EventListener
from services.receiver import EventReceiver


def get_monitored_event():
    with open(settings.abi_file) as abi_file:
        monitored_event = MonitoredEvent(
            contract_address=Web3.to_checksum_address(settings.contract_address),
            abi=json.load(abi_file),
            event_name=settings.event_name,
            receiver=EventReceiver()
        )
    return monitored_event


def monitor_total_distribution_events():
    listener = EventListener(
        monitored_event=get_monitored_event(),
        rpc=settings.eth_rpc,
    )
    listener.run()
