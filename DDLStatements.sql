/**File for DDL Statements in Capstone Project Database**/

/**Tables**/

CREATE TABLE assets (
    asset_id    SERIAL,
    symbol      VARCHAR(10),
    name        VARCHAR(50),
    asset_type  VARCHAR(10),
    CONSTRAINT assets_pkey PRIMARY KEY (asset_id),
    CONSTRAINT uq_symbol UNIQUE (symbol)
);

CREATE TABLE crypto (
    asset_id                INT,
    market_rank             INT,
    blockchain_platform     VARCHAR(50),
    consensus_mechanism     VARCHAR(20),
    all_time_high           NUMERIC,          
    all_time_low            NUMERIC,          
    all_time_high_date      TIMESTAMPTZ,      
    all_time_low_date       TIMESTAMPTZ,     
    last_updated            TIMESTAMPTZ,      
    CONSTRAINT crypto_pkey PRIMARY KEY (asset_id),
    CONSTRAINT crypto_fkey FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE stocks (
    asset_id    INT,
    exchange    VARCHAR(50),
    sector      VARCHAR(50),
    week_52_high        NUMERIC,
    week_52_low         NUMERIC,
    last_updated        TIMESTAMPTZ,
    CONSTRAINT stocks_pkey PRIMARY KEY (asset_id),
    CONSTRAINT stocks_fkey FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE price_history (
    price_id    SERIAL,
    asset_id    INT,
    price_usd   NUMERIC,
    recorded_at   TIMESTAMPTZ,
    CONSTRAINT price_history_pkey PRIMARY KEY (price_id),
    CONSTRAINT price_history_fkey FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE volume_history (
        volume_id   SERIAL,
        asset_id    INT,
        volume      NUMERIC,
        recorded_at   TIMESTAMPTZ,
        CONSTRAINT volume_history_pkey PRIMARY KEY (volume_id),
        CONSTRAINT volume_history_fkey FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE market_cap_history (
        market_cap_id   SERIAL,
        asset_id        INT,
        market_cap      NUMERIC,
        recorded_at       TIMESTAMPTZ,
        CONSTRAINT market_cap_history_pkey PRIMARY KEY (market_cap_id),
        CONSTRAINT market_cap_history_fkey FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE

);

CREATE TABLE change_metrics (
        metric_id       SERIAL,
        asset_id        INT,
        price_change_24h     NUMERIC, 
        price_change_percent_24h    NUMERIC,
        market_cap_change_24h     NUMERIC,
        market_cap_change_percent_24h   NUMERIC,
        recorded_at       TIMESTAMPTZ,
        CONSTRAINT price_change_metrics_pkey PRIMARY KEY (metric_id),
        CONSTRAINT price_change_metrics_fkey FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

CREATE TABLE global_crypto_stats (
        stat_id     SERIAL,
        total_crypto_market_cap     NUMERIC,
        total_crypto_volume        NUMERIC,
        recorded_at   TIMESTAMPTZ,
        CONSTRAINT global_crypto_stats_pkey PRIMARY KEY (stat_id)

);

CREATE TABLE ohlc_history (
    ohlc_id     SERIAL,
    asset_id    INT,
    open        NUMERIC,
    high        NUMERIC,
    low         NUMERIC,
    close       NUMERIC,
    recorded_at TIMESTAMPTZ,
    CONSTRAINT ohlc_history_pkey PRIMARY KEY (ohlc_id),
    CONSTRAINT ohlc_history_fkey FOREIGN KEY (asset_id) REFERENCES assets (asset_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


CREATE INDEX idx_price_asset_time 
ON price_history (asset_id, recorded_at);

CREATE INDEX idx_volume_asset_time 
ON volume_history (asset_id, recorded_at);

CREATE INDEX idx_market_cap_asset_time
ON market_cap_history (asset_id, recorded_at);

CREATE INDEX idx_change_metrics_asset_time
ON change_metrics (asset_id, recorded_at);

CREATE INDEX idx_global_crypto_stats_time
ON global_crypto_stats (recorded_at);

CREATE INDEX idx_ohlc_asset_time
ON ohlc_history (asset_id, recorded_at);