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

    try:
        timestamp = datetime.now(timezone.utc)

        global_url = "https://api.coingecko.com/api/v3/global"
        response = requests.get(global_url, headers=headers)

        if response.status_code != 200:
            print(f"CoinGecko global API error: {response.status_code}")
            return {"statusCode": 500, "body": "CoinGecko global API error"}

        global_data = response.json().get("data", {})

        total_crypto_market_cap = global_data.get("total_market_cap", {}).get("usd")
        total_crypto_volume = global_data.get("total_volume", {}).get("usd")

        if any(v is None for v in [total_crypto_market_cap, total_crypto_volume]):
            print("Missing fields in CoinGecko global response")
            return {"statusCode": 500, "body": "Missing fields in response"}

        cur.execute(
            """INSERT INTO global_crypto_stats (
                total_crypto_market_cap,
                total_crypto_volume,
                recorded_at
            ) VALUES (%s, %s, %s)""",
            (total_crypto_market_cap, total_crypto_volume, timestamp)
        )

        conn.commit()
        print("Global crypto stats inserted successfully!")
        return {"statusCode": 200, "body": "Global crypto stats inserted successfully!"}

    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
        return {"statusCode": 500, "body": f"Error: {e}"}

    finally:
        cur.close()
        conn.close()