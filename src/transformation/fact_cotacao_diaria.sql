DROP TABLE IF EXISTS fact_cotacao_diaria;

CREATE TABLE fact_cotacao_diaria AS

SELECT
     moeda
    ,dt_cotacao
    ,cotacao_compra
    ,cotacao_venda
    ,ROUND(
        (cotacao_compra + cotacao_venda) / 2,
        6
    ) AS cotacao_media
    ,ROUND(
        cotacao_venda - cotacao_compra,
        6
    ) AS spread
FROM currency
WHERE tp_boletim = 'Fechamento';