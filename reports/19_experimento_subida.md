# Experimento: subestimação das subidas

Gerado por `src/live/experimento_subida.py`. Mesmo arranjo do backtest (reports/18_backtest.md): treino só no passado, chuva de latência pelos postos, chuva futura arquivada D0. Regime alto, 12–24h, mesmos instantes para todos os produtos.

Seleção: ev20240430, ev20240616, ev20241012, ev20250618, ev20250922, ev20251108. Confirmação (fora da escolha): ev20260629, ev20260722. Critério fixado antes de rodar: menor MAE em subida+pico sem piorar o MAE geral em mais de 5% contra o combinado v2.

## Seleção (2024–2025)

| produto                 |    n |   mae_geral_cm |   vies_geral_cm |   mae_subida_pico_cm |   vies_subida_pico_cm |   delta_geral_pct |   delta_subida_pico_pct | aprovado   |
|:------------------------|-----:|---------------:|----------------:|---------------------:|----------------------:|------------------:|------------------------:|:-----------|
| comb hid                | 6635 |            130 |             -16 |                  183 |                  -103 |                -2 |                      -5 | True       |
| comb hid+peso           | 6635 |            129 |              -6 |                  184 |                   -90 |                -3 |                      -4 | True       |
| comb ridge_hid          | 6635 |            130 |             -17 |                  185 |                  -103 |                -2 |                      -4 | True       |
| comb peso               | 6635 |            131 |              -6 |                  191 |                   -84 |                -1 |                      -1 | True       |
| comb lt                 | 6635 |            129 |             -11 |                  192 |                   -86 |                -3 |                      -0 | True       |
| combinado v2            | 6635 |            132 |             -15 |                  193 |                   -97 |                 0 |                       0 | False      |
| ridge_hid mediana D0    | 6635 |            150 |               3 |                  193 |                   -68 |                14 |                       0 | False      |
| gbm_hid_peso mediana D0 | 6635 |            126 |             -15 |                  199 |                  -112 |                -5 |                       3 | False      |
| gbm_lt mediana D0       | 6635 |            119 |             -29 |                  200 |                  -116 |               -10 |                       4 | False      |
| gbm_peso mediana D0     | 6635 |            125 |             -18 |                  200 |                  -113 |                -5 |                       4 | False      |
| gbm_hid mediana D0      | 6635 |            132 |             -35 |                  205 |                  -139 |                -0 |                       6 | False      |
| gbm mediana D0          | 6635 |            132 |             -37 |                  210 |                  -139 |                -0 |                       9 | False      |
| ridge mediana D0        | 6635 |            156 |               7 |                  211 |                   -55 |                18 |                       9 | False      |

**Escolhido na seleção:** `comb hid`.

## Confirmação (2026)

| produto                 |    n |   mae_geral_cm |   vies_geral_cm |   mae_subida_pico_cm |   vies_subida_pico_cm |   delta_geral_pct |   delta_subida_pico_pct | aprovado   |
|:------------------------|-----:|---------------:|----------------:|---------------------:|----------------------:|------------------:|------------------------:|:-----------|
| comb hid+peso           | 2282 |            102 |             -33 |                  195 |                  -175 |                -7 |                     -14 | True       |
| gbm_hid_peso mediana D0 | 2282 |             99 |             -43 |                  197 |                  -176 |                -9 |                     -14 | True       |
| ridge_hid mediana D0    | 2282 |            126 |             -24 |                  202 |                  -173 |                16 |                     -11 | False      |
| comb hid                | 2282 |            105 |             -37 |                  207 |                  -192 |                -3 |                      -9 | True       |
| gbm_lt mediana D0       | 2282 |             97 |             -48 |                  209 |                  -192 |               -11 |                      -8 | True       |
| comb ridge_hid          | 2282 |            107 |             -39 |                  212 |                  -197 |                -2 |                      -7 | True       |
| comb lt                 | 2282 |            103 |             -49 |                  214 |                  -203 |                -5 |                      -6 | True       |
| gbm_peso mediana D0     | 2282 |            109 |             -46 |                  214 |                  -192 |                -0 |                      -6 | True       |
| comb peso               | 2282 |            106 |             -48 |                  219 |                  -203 |                -2 |                      -4 | True       |
| gbm_hid mediana D0      | 2282 |            108 |             -50 |                  224 |                  -210 |                -1 |                      -2 | True       |
| combinado v2            | 2282 |            109 |             -53 |                  228 |                  -218 |                 0 |                       0 | False      |
| ridge mediana D0        | 2282 |            127 |             -51 |                  233 |                  -215 |                17 |                       2 | False      |
| gbm mediana D0          | 2282 |            114 |             -54 |                  234 |                  -221 |                 5 |                       2 | False      |

## Escolhido × combinado v2 × operacional (todos os eventos, 12h)

| produto      |   h |    n |   mae_cm |   vies_cm |   mae_persistencia_cm |   skill |
|:-------------|----:|-----:|---------:|----------:|----------------------:|--------:|
| comb hid     |  12 | 3283 |       82 |        -8 |                   186 |    0.56 |
| combinado v2 |  12 | 3283 |       82 |       -10 |                   186 |    0.56 |
| operacional  |  12 | 3283 |       83 |       -14 |                   186 |    0.56 |

## Escolhido × combinado v2 por evento (12–24h)

| evento     | produto      |    n |   mae_cm |   vies_cm |   mae_persistencia_cm |   skill |
|:-----------|:-------------|-----:|---------:|----------:|----------------------:|--------:|
| ev20240430 | comb hid     | 2447 |      231 |        29 |                   270 |    0.15 |
| ev20240430 | combinado v2 | 2447 |      224 |        21 |                   270 |    0.17 |
| ev20240616 | comb hid     | 2163 |       83 |       -15 |                   188 |    0.56 |
| ev20240616 | combinado v2 | 2163 |       82 |       -20 |                   188 |    0.56 |
| ev20241012 | comb hid     |  310 |       61 |       -57 |                   148 |    0.59 |
| ev20241012 | combinado v2 |  310 |       71 |       -68 |                   148 |    0.52 |
| ev20250618 | comb hid     | 2524 |      127 |       -24 |                   269 |    0.53 |
| ev20250618 | combinado v2 | 2524 |      130 |       -19 |                   269 |    0.52 |
| ev20250922 | comb hid     |  591 |       43 |       -26 |                   187 |    0.77 |
| ev20250922 | combinado v2 |  591 |       45 |       -15 |                   187 |    0.76 |
| ev20251108 | comb hid     |  552 |       59 |        12 |                   220 |    0.73 |
| ev20251108 | combinado v2 |  552 |       70 |         3 |                   220 |    0.68 |
| ev20260629 | comb hid     |  625 |       36 |       -17 |                   156 |    0.77 |
| ev20260629 | combinado v2 |  625 |       46 |       -35 |                   156 |    0.7  |
| ev20260722 | comb hid     | 1790 |      125 |       -41 |                   400 |    0.69 |
| ev20260722 | combinado v2 | 1790 |      126 |       -55 |                   400 |    0.68 |

## Por fase (12–24h, todos os eventos)

| produto      | fase     |    n |   mae_cm |   vies_cm |   mae_persistencia_cm |   skill |
|:-------------|:---------|-----:|---------:|----------:|----------------------:|--------:|
| comb hid     | pico     |  439 |      156 |       -93 |                   444 |    0.65 |
| comb hid     | recessao | 8035 |      103 |        27 |                   208 |    0.5  |
| comb hid     | subida   | 2528 |      193 |      -122 |                   386 |    0.5  |
| combinado v2 | pico     |  439 |      176 |      -105 |                   444 |    0.6  |
| combinado v2 | recessao | 8035 |      100 |        20 |                   208 |    0.52 |
| combinado v2 | subida   | 2528 |      203 |      -119 |                   386 |    0.47 |
