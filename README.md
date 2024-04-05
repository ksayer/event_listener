# DistributorEventListener

## Functional
- Reads events (TotalDistribution) from the contract (0xaBE235136562a5C2B02557E1CaE7E8c85F2a5da0) in Ethereum that occurred in the last 24 hours.
- Calculate and send the daily sum of all four parameters through the bot to a Telegram chat. 
By default, sends notification every 4h.
- Record all events in a PostgreSQL database

## Installing

 - python 3.11
 - pip install -r requirements.txt
    
Create `.env` file with next values:


    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_HOST=
    POSTGRES_PORT=
    POSTGRES_DB=
    TG_TOKEN=
    TG_CHAT_ID=
    ETH_RPC=
    
    NOTIFICATION_PERIOD=default is 14400 seconds (send notification every 4 hours)


### Usage

`python main.py`

### Tests

`python -m pytest`