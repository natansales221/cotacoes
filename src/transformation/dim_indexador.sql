DROP TABLE IF EXISTS dim_indexador;

CREATE TABLE dim_indexador
(
    indexador_id        TEXT PRIMARY KEY,
    codigo_fonte        TEXT,
    nome_indexador      TEXT NOT NULL,
    categoria           TEXT NOT NULL,
    periodicidade       TEXT NOT NULL,
    unidade             TEXT NOT NULL,
    fonte               TEXT
);

INSERT INTO dim_indexador
(
    indexador_id,
    codigo_fonte,
    nome_indexador,
    categoria,
    periodicidade,
    unidade,
    fonte
)
VALUES
    ('SELIC',    '1178',  'Selic',              'JUROS',    'DIARIA', 'PERCENTUAL_AA',     'Banco Central do Brasil - SGS'),
    ('IPCA',     '433',   'IPCA',               'INFLACAO', 'MENSAL', 'PERCENTUAL_MENSAL', 'Banco Central do Brasil - SGS'),
    ('IBOVESPA', '^BVSP', 'Ibovespa',           'BOLSA',    'DIARIA', 'PONTOS',            'Yahoo Finance via yfinance'),
    ('SP500',    '^GSPC', 'S&P 500',            'BOLSA',    'DIARIA', 'PONTOS',            'Yahoo Finance via yfinance'),
    ('NASDAQ',   '^IXIC', 'Nasdaq Composite',   'BOLSA',    'DIARIA', 'PONTOS',            'Yahoo Finance via yfinance');