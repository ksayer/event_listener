import json

from web3 import Web3

from services.listener import MonitoredEvent, EventListener
from services.receiver import EventReceiver


def get_monitored_event():
    with open('core/abi.json') as abi_file:
        monitored_event = MonitoredEvent(
            contract_address=Web3.to_checksum_address("0xaBE235136562a5C2B02557E1CaE7E8c85F2a5da0"),
            abi=json.load(abi_file),
            event_name='TotalDistribution',
            receiver=EventReceiver()
        )
    return monitored_event


def monitor_total_distribution_events():
    listener = EventListener(
        monitored_event=get_monitored_event(),
        rpc='https://eth.drpc.org',
    )
    listener.run()
