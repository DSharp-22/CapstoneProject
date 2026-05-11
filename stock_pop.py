import requests
import psycopg2
from datetime import datetime, timezone, time
import pytz

def lambda_handler(event, context):
    est = pytz.timezone("US/Eastern")
    now_est = datetime.now(est)

    # Skip if outside market hours 
    if now_est.weekday() >= 5 or not (time(9, 30) <= now_est.time() <= time(16, 0)):
        print("Outside market hours — skipping run.")
        return {"statusCode": 200, "body": "Outside market hours — skipping run."}

    conn = psycopg2.connect(
        host = "*****",
        dbname = "*****",
        user = "*****",
        password = "*****"
    )

    cur = conn.cursor()

    FINNHUB_API_KEY = "API_KEY_HERE"

    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA"]

    try:
        timestamp = datetime.now(timezone.utc)

        for symbol in symbols:

            # Quote endpoint
            quote_url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
            response = requests.get(quote_url)

            if response.status_code != 200:
                print(f"API Error for {symbol}: {response.status_code}")
                continue

            data = response.json()

            price = data["c"]
            prev_close = data["pc"]
            open_price = data["o"]
            high = data["h"]
            low = data["l"]

            # Metrics endpoint for volume and 52-week high/low
            metrics_url = f"https://finnhub.io/api/v1/stock/metric?symbol={symbol}&metric=all&token={FINNHUB_API_KEY}"
            metrics_response = requests.get(metrics_url)

            if metrics_response.status_code != 200:
                print(f"Metrics API Error for {symbol}: {metrics_response.status_code}")
                continue

            metrics_data = metrics_response.json().get("metric", {})

            volume = metrics_data.get("10DayAverageTradingVolume")
            week_52_high = metrics_data.get("52WeekHigh")
            week_52_low = metrics_data.get("52WeekLow")

            # Null guard - ensures all information is gathered rather than bits and pieces
            if any(v is None for v in [price, prev_close, volume]):
                print(f"Skipping {symbol} — missing fields in API response")
                continue

            # Calculate change metrics
            price_change = price - prev_close
            price_change_percent = ((price - prev_close) / prev_close) * 100 if prev_close else None

         
            cur.execute("SELECT asset_id FROM assets WHERE symbol = %s", (symbol,))
            asset_id = cur.fetchone()[0]

            # Price History
            cur.execute(
                "INSERT INTO price_history (asset_id, price_usd, recorded_at) VALUES (%s, %s, %s)",
                (asset_id, price, timestamp)
            )

            # Volume History
            cur.execute(
                "INSERT INTO volume_history (asset_id, volume, recorded_at) VALUES (%s, %s, %s)",
                (asset_id, volume, timestamp)
            )

            # Change Metrics
            cur.execute(
                """INSERT INTO change_metrics (
                    asset_id, price_change_24h, price_change_percent_24h,
                    market_cap_change_24h, market_cap_change_percent_24h, recorded_at
                ) VALUES (%s, %s, %s, %s, %s, %s)""",
                (asset_id, price_change, price_change_percent, None, None, timestamp)
            )

            # OHLC
            cur.execute(
                """INSERT INTO ohlc_history (asset_id, open, high, low, close, recorded_at)
                VALUES (%s, %s, %s, %s, %s, %s)""",
                (asset_id, open_price, high, low, price, timestamp)
            )

            # 52-week high/low — only update if changed
            cur.execute(
                "SELECT week_52_high, week_52_low FROM stocks WHERE asset_id = %s",
                (asset_id,)
            )
            #Grabbing current 52 week highs and lows
            current_52_high, current_52_low = cur.fetchone()
            #Comparing highs and lows to what is already stored in DB - updates if changed
            if current_52_high != week_52_high or current_52_low != week_52_low:
                cur.execute(
                    """UPDATE stocks
                    SET week_52_high = %s,
                        week_52_low = %s,
                        last_updated = %s
                    WHERE asset_id = %s""",
                    (week_52_high, week_52_low, timestamp, asset_id)
                )
                print(f"52-week high/low updated for {symbol}")

        conn.commit()
        print("Stock data inserted successfully!")

    except Exception as e:
        print(f"Error during insert: {e}")
        conn.rollback()

    finally:
        cur.close()
        conn.close()