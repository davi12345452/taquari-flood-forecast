# Revisão da rodada de 04/11/2026 14:00

Modo: **emissao**. Referência observada: 04/11 14:00 (UTC−3). Emissão registrada em 04/11/2026 15:17:25 local. A antecedência real desconta o tempo desde a observação.

Horizontes contados desde a referência da própria estação; chuva e ONS mantêm seus atrasos no treino e na inferência. Alterações de modelo passam por comparação por fase da cheia. A coluna de cota é uma estimativa pontual, não uma cota de pico. Não é sistema de alerta.

| alvo      | motor          |   h | referencia_local   |   observado_cm |   previsto_cm | validade_local   |   antecedencia_real_h | status     |
|:----------|:---------------|----:|:-------------------|---------------:|--------------:|:-----------------|----------------------:|:-----------|
| Muçum     | linear         |   3 | 04/11 14:00        |            331 |         318.2 | 04/11 17:00      |                   1.7 | estimativa |
| Muçum     | gbm_delta      |   6 | 04/11 14:00        |            331 |         362.5 | 04/11 20:00      |                   4.7 | estimativa |
| Muçum     | gbm_delta      |   9 | 04/11 14:00        |            331 |         462.2 | 04/11 23:00      |                   7.7 | estimativa |
| Muçum     | gbm_delta      |  12 | 04/11 14:00        |            331 |         553.7 | 05/11 02:00      |                  10.7 | estimativa |
| Encantado | linear         |   3 | 04/11 14:00        |            262 |         284.3 | 04/11 17:00      |                   1.7 | estimativa |
| Encantado | ridge_montante |   6 | 04/11 14:00        |            262 |         279.4 | 04/11 20:00      |                   4.7 | estimativa |
| Encantado | gbm_delta      |   9 | 04/11 14:00        |            262 |         365.5 | 04/11 23:00      |                   7.7 | estimativa |
| Encantado | gbm_delta      |  12 | 04/11 14:00        |            262 |         417.5 | 05/11 02:00      |                  10.7 | estimativa |
| Estrela   | linear         |   3 | 04/11 14:00        |           1312 |        1316.5 | 04/11 17:00      |                   1.7 | estimativa |
| Estrela   | linear         |   6 | 04/11 14:00        |           1312 |        1335.5 | 04/11 20:00      |                   4.7 | estimativa |
| Estrela   | linear         |   9 | 04/11 14:00        |           1312 |        1351.4 | 04/11 23:00      |                   7.7 | estimativa |
| Estrela   | linear         |  12 | 04/11 14:00        |           1312 |        1362.4 | 05/11 02:00      |                  10.7 | estimativa |

## Faixas e diagnóstico

As faixas usam o quantil 90% dos erros de 2025, separado por regime, sem garantia de cobertura. Não são publicadas quando há menos de 30 pares, a velocidade está fora da calibração ou a cobertura dos últimos erros conhecidos cai abaixo de 80% (mínimo três pares nas últimas seis horas). Uma faixa ausente não significa erro zero.

| alvo      |   h | inferior_cm   | superior_cm   | faixa_status                   | cobertura_recente_pct   |   n_faixa_recente |
|:----------|----:|:--------------|:--------------|:-------------------------------|:------------------------|------------------:|
| Muçum     |   3 | —             | —             | sem calibração                 | —                       |                 0 |
| Muçum     |   6 | 316.6         | 408.5         | empírica, sem garantia         | 100.0                   |                 6 |
| Muçum     |   9 | 385.8         | 538.5         | empírica, sem garantia         | 83.3                    |                 6 |
| Muçum     |  12 | 447.1         | 660.3         | empírica, sem garantia         | 83.3                    |                 6 |
| Encantado |   3 | —             | —             | sem calibração                 | —                       |                 0 |
| Encantado |   6 | —             | —             | erros recentes excedem a faixa | 66.7                    |                 6 |
| Encantado |   9 | —             | —             | erros recentes excedem a faixa | 33.3                    |                 6 |
| Encantado |  12 | —             | —             | erros recentes excedem a faixa | 16.7                    |                 6 |
| Estrela   |   3 | —             | —             | sem calibração                 | —                       |                 0 |
| Estrela   |   6 | 1303.3        | 1367.6        | empírica, sem garantia         | 100.0                   |                 6 |
| Estrela   |   9 | —             | —             | erros recentes excedem a faixa | 50.0                    |                 6 |
| Estrela   |  12 | 1288.7        | 1436.0        | empírica, sem garantia         | 100.0                   |                 6 |

![Hidrograma revisado](figs/live_v3_20261104_17.png)

## Replay da subida

Referências a partir de 03/11 14:00; somente alvos já observados. Horizontes maiores têm menos pares. Ausência de linha significa ausência de pares, não erro zero.

| alvo      |   h |   MAE_cm |   vies_cm |   n |
|:----------|----:|---------:|----------:|----:|
| Encantado |   3 |     15.3 |      -6.4 |  22 |
| Encantado |   6 |     38   |      -9.5 |  19 |
| Encantado |   9 |     55.2 |     -44.5 |  16 |
| Encantado |  12 |     74.8 |     -70.8 |  13 |
| Estrela   |   3 |     11.3 |       3.9 |  22 |
| Estrela   |   6 |     10.4 |       4   |  19 |
| Estrela   |   9 |     23.6 |       1.7 |  16 |
| Estrela   |  12 |     22.7 |     -15.1 |  13 |
| Muçum     |   3 |     35.4 |      -1   |  22 |
| Muçum     |   6 |     21.8 |      -3.1 |  19 |
| Muçum     |   9 |     37.3 |     -31.1 |  16 |
| Muçum     |  12 |     86.8 |     -86.8 |  13 |

Os candidatos são escolhidos em 2023–2024, confirmados em 2025 e podem ser vetados por regressão em 2026. A comparação completa está em [melhoria e aceitação](12_melhoria_live.md). O replay assume atrasos fixos e não recompõe a publicação real de cada fonte.

Arquivo local da execução: `data/processed/live_runs/emissao_20261104T181725138058Z`. Contém previsões, replay, features, datasets de treino, código e configuração.

## Emissões reais conferidas

| alvo      |   h |   MAE_cm |   n |
|:----------|----:|---------:|----:|
| Encantado |   3 |     28.2 |  37 |
| Encantado |   6 |     88.2 |  35 |
| Encantado |   9 |    112.8 |  36 |
| Encantado |  12 |    126.3 |  36 |
| Estrela   |   3 |     14.5 |  38 |
| Estrela   |   6 |     39.5 |  36 |
| Estrela   |   9 |     73.6 |  36 |
| Estrela   |  12 |    113.7 |  36 |
| Muçum     |   3 |     47.9 |   5 |
| Muçum     |   6 |     92.7 |  36 |
| Muçum     |   9 |    137.7 |  36 |
| Muçum     |  12 |    166.6 |  36 |
