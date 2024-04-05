from datetime import datetime, timezone, timedelta

from database.models import TotalDistribution


class ReportService:
    def __init__(self, distributions: list[TotalDistribution]):
        self.aix_processed = 0
        self.aix_distributed = 0
        self.eth_bought = 0
        self.eth_distributed = 0
        self.first_tx = None
        self.last_tx = None

        self.distributions = distributions

    def create(self):
        if not self.distributions:
            return 'No data available'
        for dist in self.distributions:
            self.aix_processed += dist.aix_processed
            self.aix_distributed += dist.aix_distributed
            self.eth_bought += dist.eth_bought
            self.eth_distributed += dist.eth_distributed

        self._fill_time(self.distributions[0].created, self.distributions[-1].created)
        return self._create_message()

    def _create_message(self):
        return f"""Daily $AIX Stats:
        - First TX: {self.first_tx}
        - Last TX: {self.last_tx}
        - AIX processed: {self._format_number(self.aix_processed)}
        - AIX distributed:  {self._format_number(self.aix_distributed)}
        - ETH bought:  {self._format_number(self.eth_bought)}
        - ETH distributed:  {self._format_number(self.eth_distributed)}
        """

    def _fill_time(self, first_txn: datetime, last_txn: datetime):
        now = datetime.now(tz=timezone.utc)
        self.first_tx = self._format_time((now - first_txn).seconds)
        self.last_tx = self._format_time((now - last_txn).seconds)

    @staticmethod
    def _format_number(number: int) -> str:
        return f'{number / 10 ** 18:,.2f}'

    @staticmethod
    def _format_time(seconds: int) -> str:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h{minutes}m ago"
