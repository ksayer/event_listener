import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime

from services.receiver import EventReceiver


@pytest.fixture
def mock_event():
    return {
        'args': {
            'inputAixAmount': 100,
            'distributedAixAmount': 50,
            'swappedEthAmount': 20,
            'distributedEthAmount': 10
        },
        'blockNumber': 12345,
        'transactionHash': '0xhash'
    }


@pytest.fixture
def mock_web3():
    mock_w3 = MagicMock()
    mock_w3.eth.get_block.return_value = {'timestamp': datetime.now().timestamp()}
    mock_w3.eth.get_transaction_receipt.return_value = {'from': '0xfrom'}
    return mock_w3


@patch('services.receiver.TotalDistribution.create')
def test_event_receiver_save(mock_create, mock_event, mock_web3):
    receiver = EventReceiver()
    receiver.save(mock_event, mock_web3)

    mock_create.assert_called_once()
    call_args = mock_create.call_args[1]

    assert call_args['aix_processed'] == mock_event['args']['inputAixAmount']
    assert call_args['aix_distributed'] == mock_event['args']['distributedAixAmount']
    assert call_args['eth_bought'] == mock_event['args']['swappedEthAmount']
    assert call_args['eth_distributed'] == mock_event['args']['distributedEthAmount']
    assert call_args['distributor'] == mock_web3.eth.get_transaction_receipt.return_value['from']
