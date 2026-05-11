import requests
import psycopg2
from datetime import datetime, timezone

def lambda_handler(event, context):
    conn = psycopg2.connect(
        host = "*****",
        dbname = "*****",
        user = "*****",
        password = "*****"
    )

    cur = conn.cursor()

    headers = {"x-cg-demo-api-key": "API_KEY_HERE"}

    # Coin ID to symbol mapping - OHLC endpoint uses coin ID
    # assets table is keyed by symbol
    coins = {
        "bitcoin": "BTC",
        "ethereum": "ETH",
        "solana": "SOL",
        "tether": "USDT",
        "binancecoin": "BNB",
        "ripple": "XRP",
        "usd-coin": "USDC",
        "tron": "TRX",
        "hyperliquid": "HYPE",
        "cardano": "ADA"
    }

    try:
        for coin_id, symbol in coins.items():

            ohlc_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/ohlc"
            ohlc_params = {"vs_currency": "usd", "days": "1"}
            response = requests.get(ohlc_url, params=ohlc_params, headers=headers)

            if response.status_code != 200:
                print(f"OHLC API Error for {symbol}: {response.status_code}")
                continue

            ohlc_data = response.json()

            if not ohlc_data:
                print(f"No OHLC data returned for {symbol}, skipping.")
                continue

            # Look up asset_id
            cur.execute("SELECT asset_id FROM assets WHERE symbol = %s", (symbol,))
            asset_id = cur.fetchone()[0]

            # Each candle is [timestamp_ms, open, high, low, close]
            # Grab only the most recent candle
            latest = ohlc_data[-1]
            ohlc_timestamp = datetime.fromtimestamp(latest[0] / 1000, tz=timezone.utc)
            open_price = latest[1]
            high = latest[2]
            low = latest[3]
            close = latest[4]

            # Null guard - ensures all information is gathered rather than bits and pieces
            if any(v is None for v in [open_price, high, low, close]):
                print(f"Skipping {symbol} — missing OHLC fields in response")
                continue

            cur.execute(
                """INSERT INTO ohlc_history (asset_id, open, high, low, close, recorded_at)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (asset_id, open_price, high, low, close, ohlc_timestamp)
            )

        conn.commit()
        print("Crypto OHLC data inserted successfully!")
        return {"statusCode": 200, "body": "Crypto OHLC data inserted successfully!"}

    except Exception as e:
        print(f"Error during insert: {e}")
        conn.rollback()
        return {"statusCode": 500, "body": f"Error: {e}"}

    finally:
        cur.close()
        conn.close()