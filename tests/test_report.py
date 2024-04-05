from datetime import datetime, timezone, timedelta
from unittest.mock import patch, MagicMock

import pytest

from services.report import ReportService, get_report


@pytest.fixture
def mock_distribution():
    return MagicMock(
        aix_processed=100,
        aix_distributed=50,
        eth_bought=20,
        eth_distributed=10,
        created=datetime.now(tz=timezone.utc) - timedelta(hours=1),
        distributor='0x123'
    )


@patch('services.report.TotalDistribution.filter_by_created')
def test_get_report_with_data(mock_filter, mock_distribution):
    mock_filter.return_value = [mock_distribution]
    with patch('services.report.get_eth_balance', return_value=5 * 10**18):
        report = get_report()
    assert 'AIX processed: 0.00' in report
    assert 'Distributor balance: 5.00' in report  # Предполагая, что balance = 500 / 10**18


def test_report_service_create_message(mock_distribution):
    distributions = [mock_distribution]
    report_service = ReportService(distributions)
    with patch('services.report.get_eth_balance', return_value=5 * 10**18):
        message = report_service.create()
    assert 'AIX processed: 0.00' in message
    assert 'Distributor balance: 5.00' in message