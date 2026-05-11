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

    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,solana,tether,binancecoin,ripple,usd-coin,tron,hyperliquid,cardano"
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code != 200:
        print(f"API Error: {response.status_code} - {response.text}")
        cur.close()
        conn.close()
        exit()  # Stops the script cleanly instead of crashing

    data = response.json()


    try:
        timestamp = datetime.now(timezone.utc)

        for coin in data:
            name = coin["name"]
            symbol = coin["symbol"].upper()
            price = coin["current_price"]
            volume = coin["total_volume"]
            market_cap = coin["market_cap"]
            price_change_24h = coin["price_change_24h"]
            p_c_percent = coin["price_change_percentage_24h"]
            market_cap_change_24h = coin["market_cap_change_24h"]
            mk_c_percent = coin["market_cap_change_percentage_24h"]
            all_time_high = coin["ath"]
            ath_date = datetime.fromisoformat(coin["ath_date"].replace("Z", "+00:00"))
            all_time_low = coin["atl"]
            atl_date = datetime.fromisoformat(coin["atl_date"].replace("Z", "+00:00"))

            # Null Guard - ensures all information is gathered rather than bits and pieces 
            if any(v is None for v in [price, volume, market_cap, price_change_24h,
                                        p_c_percent, market_cap_change_24h, mk_c_percent,
                                        coin["market_cap_rank"]]):
                print(f"Skipping {symbol} — missing fields in API response")
                continue

            # Assets
            cur.execute(
                "SELECT asset_id FROM assets WHERE symbol = %s",
                (symbol,)
            )

            result = cur.fetchone()


            asset_id = result[0]

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

            # Market Cap History
            cur.execute(
                "INSERT INTO market_cap_history (asset_id, market_cap, recorded_at) VALUES (%s, %s, %s)",
                (asset_id, market_cap, timestamp)
            )
            # Change Metrics
            cur.execute(
                """INSERT INTO change_metrics (
                    asset_id, price_change_24h, price_change_percent_24h,
                    market_cap_change_24h, market_cap_change_percent_24h, recorded_at
                ) VALUES (%s, %s, %s, %s, %s, %s)""",
                (asset_id, price_change_24h, p_c_percent,
                market_cap_change_24h, mk_c_percent, timestamp)
            )

            cur.execute("SELECT all_time_high, all_time_low FROM crypto WHERE asset_id = %s",
                        (asset_id,)
            )
            
            crypto_row = cur.fetchone()
            #Grabbing ath and atl from coin with info currently being ingested
            current_ath, current_atl = crypto_row
            #Comparing current ath and atl with what is already stored in DB - if different it updates 
            if current_ath != all_time_high or current_atl != all_time_low:
                cur.execute(
                    """UPDATE crypto
                    SET all_time_high = %s,
                    all_time_low = %s,
                    all_time_high_date = %s,
                    all_time_low_date = %s,
                    last_updated = %s
                    WHERE asset_id = %s""",
                    (all_time_high, all_time_low, ath_date, atl_date, timestamp, asset_id)
                )
                print(f"ATH/ATL updated for {symbol}")

            # Market rank update — only update if value has changed
            cur.execute(
                "SELECT market_rank FROM crypto WHERE asset_id = %s",
                (asset_id,)
            )
            current_rank = cur.fetchone()[0]
            new_rank = coin["market_cap_rank"]

            if current_rank != new_rank:
                cur.execute(
                    """UPDATE crypto
                    SET market_rank = %s,
                        last_updated = %s
                    WHERE asset_id = %s""",
                    (new_rank, timestamp, asset_id)
                )
                print(f"Market rank updated for {symbol}: {current_rank} -> {new_rank}")

        conn.commit()
        print("Data inserted successfully!")

    # catches any DB or parsing error
    except Exception as e:
        print(f"Error during insert: {e}")
        conn.rollback()  # Roll back any partial writes from this run

    finally:
        cur.close()
        conn.close()