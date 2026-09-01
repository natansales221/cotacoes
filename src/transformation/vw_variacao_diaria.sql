DROP VIEW IF EXISTS vw_variacao_diaria;

CREATE VIEW vw_variacao_diaria AS

WITH cotacao_anterior AS (
    SELECT
         moeda
        ,dt_cotacao
        ,cotacao_compra
        ,cotacao_venda
        ,cotacao_media
        ,spread
        ,LAG(cotacao_media) OVER (
            PARTITION BY moeda
            ORDER BY dt_cotacao
        ) AS cotacao_media_anterior
    FROM fact_cotacao_diaria
)

SELECT
     moeda
    ,dt_cotacao
    ,cotacao_compra
    ,cotacao_venda
    ,cotacao_media
    ,spread
    ,cotacao_media_anterior
    ,ROUND(
        (
            (cotacao_media - cotacao_media_anterior)
            / NULLIF(cotacao_media_anterior, 0)
        ) * 100,
        4
    ) AS variacao_percentual
FROM cotacao_anterior;