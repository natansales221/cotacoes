DROP TABLE IF EXISTS fact_indexador;

CREATE TABLE fact_indexador
(
    data            TEXT NOT NULL,
    indexador_id    TEXT NOT NULL,
    valor           REAL NOT NULL,
    dt_carga        TEXT,
    
    UNIQUE(indexador_id, data)
);

INSERT INTO fact_indexador
(
    data,
    indexador_id,
    valor,
    dt_carga
)

SELECT
     dt_cotacao
    ,'SELIC'
    ,vl_cotacao
    ,dt_carga
FROM selic

UNION ALL

SELECT
     data
    ,'IPCA'
    ,valor_percentual
    ,dt_carga
FROM ipca

UNION ALL

SELECT
     data
    ,'IBOVESPA'
    ,fechamento_ajustado
    ,dt_carga
FROM ibovespa
WHERE fechamento_ajustado IS NOT NULL

UNION ALL

SELECT
     data
    ,'SP500'
    ,fechamento_ajustado
    ,dt_carga
FROM sp500
WHERE fechamento_ajustado IS NOT NULL

UNION ALL

SELECT
     data
    ,'NASDAQ'
    ,fechamento_ajustado
    ,dt_carga
FROM nasdaq
WHERE fechamento_ajustado IS NOT NULL;