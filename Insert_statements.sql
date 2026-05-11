INSERT INTO assets (symbol, name, asset_type)
VALUES
    ('BTC',  'Bitcoin',        'crypto'),
    ('ETH',  'Ethereum',       'crypto'),
    ('SOL',  'Solana',         'crypto'),
    ('USDT', 'Tether',         'crypto'),
    ('BNB',  'BNB',            'crypto'),
    ('XRP',  'XRP',            'crypto'),
    ('USDC', 'USDC',           'crypto'),
    ('TRX',  'TRON',           'crypto'),
    ('HYPE', 'Hyperliquid',    'crypto'),
    ('ADA',  'Cardano',        'crypto'),
    ('AAPL', 'Apple',          'stock'),
    ('MSFT', 'Microsoft',      'stock'),
    ('GOOGL','Alphabet',       'stock'),
    ('AMZN', 'Amazon',         'stock'),
    ('NVDA', 'Nvidia',         'stock'),
    ('META', 'Meta Platforms', 'stock'),
    ('TSLA', 'Tesla',          'stock');

INSERT INTO crypto (asset_id, market_rank, blockchain_platform, consensus_mechanism)
VALUES
    ((SELECT asset_id FROM assets WHERE symbol = 'BTC'),  1,  'Bitcoin',    'PoW'),
    ((SELECT asset_id FROM assets WHERE symbol = 'ETH'),  2,  'Ethereum',   'PoS'),
    ((SELECT asset_id FROM assets WHERE symbol = 'USDT'), 3,  'Multi-chain','PoS'),
    ((SELECT asset_id FROM assets WHERE symbol = 'XRP'),  4,  'XRP Ledger', 'PBFT'),
    ((SELECT asset_id FROM assets WHERE symbol = 'BNB'),  5,  'BNB Chain',  'PoSA'),
    ((SELECT asset_id FROM assets WHERE symbol = 'USDC'), 6,  'Multi-chain','PoS'),
    ((SELECT asset_id FROM assets WHERE symbol = 'SOL'),  7,  'Solana',     'PoH'),
    ((SELECT asset_id FROM assets WHERE symbol = 'TRX'),  8,  'TRON',       'DPoS'),
    ((SELECT asset_id FROM assets WHERE symbol = 'ADA'),  9,  'Cardano',    'PoS'),
    ((SELECT asset_id FROM assets WHERE symbol = 'HYPE'), 13, 'Hyperliquid','PoS');

    INSERT INTO stocks (asset_id, exchange, sector)
VALUES
    ((SELECT asset_id FROM assets WHERE symbol = 'AAPL'),  'NASDAQ', 'Technology'),
    ((SELECT asset_id FROM assets WHERE symbol = 'MSFT'),  'NASDAQ', 'Technology'),
    ((SELECT asset_id FROM assets WHERE symbol = 'GOOGL'), 'NASDAQ', 'Technology'),
    ((SELECT asset_id FROM assets WHERE symbol = 'AMZN'),  'NASDAQ', 'Consumer Discretionary'),
    ((SELECT asset_id FROM assets WHERE symbol = 'NVDA'),  'NASDAQ', 'Technology'),
    ((SELECT asset_id FROM assets WHERE symbol = 'META'),  'NASDAQ', 'Technology'),
    ((SELECT asset_id FROM assets WHERE symbol = 'TSLA'),  'NASDAQ', 'Consumer Discretionary');