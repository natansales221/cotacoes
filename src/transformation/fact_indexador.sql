DROP TABLE IF EXISTS fact_indexador;

CREATE TABLE fact_indexador
(
    data            TEXT NOT NULL,
    indexador_id    TEXT NOT NULL,
    valor           REAL NOT NULL,
    dt_carga        TEXT,
    
    UNIQUE(indexador_id, data)
);


WITH base_indexador AS
(
    SELECT
         dt_cotacao        AS data
        ,'SELIC'           AS indexador_id
        ,vl_cotacao        AS valor
        ,dt_carga
        ,id
    FROM selic

    UNION ALL

    SELECT
         data
        ,'IPCA'
        ,valor_percentual
        ,dt_carga
        ,id
    FROM ipca

    UNION ALL

    SELECT
         data
        ,'IBOVESPA'
        ,fechamento_ajustado
        ,dt_carga
        ,id
    FROM ibovespa
    WHERE fechamento_ajustado IS NOT NULL

    UNION ALL

    SELECT
         data
        ,'SP500'
        ,fechamento_ajustado
        ,dt_carga
        ,id
    FROM sp500
    WHERE fechamento_ajustado IS NOT NULL

    UNION ALL

    SELECT
         data
        ,'NASDAQ'
        ,fechamento_ajustado
        ,dt_carga
        ,id
    FROM nasdaq
    WHERE fechamento_ajustado IS NOT NULL
),

ranking AS
(
    SELECT
         data
        ,indexador_id
        ,valor
        ,dt_carga
        ,ROW_NUMBER() OVER
        (
            PARTITION BY
                 indexador_id
                ,data
            ORDER BY
                 dt_carga DESC
                ,id DESC
        ) AS rn
    FROM base_indexador
)

INSERT INTO fact_indexador
(
     data
    ,indexador_id
    ,valor
    ,dt_carga
)

SELECT
     data
    ,indexador_id
    ,valor
    ,dt_carga
FROM ranking
WHERE rn = 1;