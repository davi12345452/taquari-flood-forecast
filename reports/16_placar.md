# Placar das emissões reais

Gerado em 05/11/2026 08:50 (UTC−3) por `src/live/placar.py`. 4983 pares previsto × observado de 42 emissões, em 3 eventos. Só entram números gravados antes da observação; replays não contam. Reexecuções com a mesma referência contam uma vez (a primeira).

`skill` = 1 − MAE/MAE da persistência nos mesmos pares: 1 é perfeito, 0 empata com repetir a cota atual, negativo é pior. `fase` é relativa ao máximo observado do alvo no evento (pico = ±3h).

## Por produto, motor e horizonte

| produto     | motor          | cenario                                 |   h |   n |   mae_cm |   vies_cm |   rmse_cm |   p90_abs_cm |   mae_persistencia_cm |   skill |
|:------------|:---------------|:----------------------------------------|----:|----:|---------:|----------:|----------:|-------------:|----------------------:|--------:|
| cenario     | gbm            | ECMWF                                   |   6 | 105 |       56 |        -4 |        80 |          142 |                   175 |    0.68 |
| cenario     | gbm            | ECMWF                                   |  12 | 105 |      109 |         6 |       136 |          244 |                   317 |    0.66 |
| cenario     | gbm            | ECMWF                                   |  18 | 102 |      109 |        27 |       138 |          245 |                   393 |    0.72 |
| cenario     | gbm            | ECMWF                                   |  24 |  93 |      108 |       -23 |       142 |          214 |                   452 |    0.76 |
| cenario     | gbm            | GEM                                     |   6 | 105 |       56 |        -6 |        81 |          144 |                   175 |    0.68 |
| cenario     | gbm            | GEM                                     |  12 | 105 |      105 |       -14 |       133 |          244 |                   317 |    0.67 |
| cenario     | gbm            | GEM                                     |  18 | 102 |      117 |         9 |       151 |          261 |                   393 |    0.7  |
| cenario     | gbm            | GEM                                     |  24 |  93 |      109 |        21 |       138 |          230 |                   452 |    0.76 |
| cenario     | gbm            | GFS                                     |   6 | 105 |       56 |        -7 |        79 |          143 |                   175 |    0.68 |
| cenario     | gbm            | GFS                                     |  12 | 105 |      101 |       -20 |       131 |          237 |                   317 |    0.68 |
| cenario     | gbm            | GFS                                     |  18 | 102 |      110 |       -16 |       143 |          250 |                   393 |    0.72 |
| cenario     | gbm            | GFS                                     |  24 |  93 |      126 |       -38 |       164 |          299 |                   452 |    0.72 |
| cenario     | gbm            | ICON                                    |   6 | 105 |       54 |        -0 |        74 |          135 |                   175 |    0.69 |
| cenario     | gbm            | ICON                                    |  12 | 105 |      100 |         7 |       125 |          214 |                   317 |    0.68 |
| cenario     | gbm            | ICON                                    |  18 | 102 |      125 |        57 |       163 |          279 |                   393 |    0.68 |
| cenario     | gbm            | ICON                                    |  24 |  93 |      140 |        31 |       178 |          312 |                   452 |    0.69 |
| cenario     | gbm            | sem mais chuva                          |   6 | 105 |       59 |       -16 |        84 |          152 |                   175 |    0.66 |
| cenario     | gbm            | sem mais chuva                          |  12 | 105 |      122 |       -46 |       155 |          260 |                   317 |    0.62 |
| cenario     | gbm            | sem mais chuva                          |  18 | 102 |      147 |       -64 |       187 |          338 |                   393 |    0.63 |
| cenario     | gbm            | sem mais chuva                          |  24 |  93 |      192 |      -125 |       245 |          408 |                   452 |    0.57 |
| cenario     | ridge          | ECMWF                                   |   6 | 105 |       50 |        -8 |        68 |          109 |                   175 |    0.71 |
| cenario     | ridge          | ECMWF                                   |  12 | 105 |       93 |        24 |       117 |          182 |                   317 |    0.71 |
| cenario     | ridge          | ECMWF                                   |  18 | 102 |      115 |        80 |       145 |          236 |                   393 |    0.71 |
| cenario     | ridge          | ECMWF                                   |  24 |  93 |      122 |        77 |       150 |          215 |                   452 |    0.73 |
| cenario     | ridge          | GEM                                     |   6 | 105 |       50 |        -4 |        68 |          108 |                   175 |    0.71 |
| cenario     | ridge          | GEM                                     |  12 | 105 |       95 |        21 |       114 |          181 |                   317 |    0.7  |
| cenario     | ridge          | GEM                                     |  18 | 102 |      122 |        81 |       153 |          241 |                   393 |    0.69 |
| cenario     | ridge          | GEM                                     |  24 |  93 |      131 |       112 |       165 |          247 |                   452 |    0.71 |
| cenario     | ridge          | GFS                                     |   6 | 105 |       51 |       -10 |        68 |          107 |                   175 |    0.71 |
| cenario     | ridge          | GFS                                     |  12 | 105 |       97 |         8 |       117 |          186 |                   317 |    0.69 |
| cenario     | ridge          | GFS                                     |  18 | 102 |      114 |        47 |       137 |          234 |                   393 |    0.71 |
| cenario     | ridge          | GFS                                     |  24 |  93 |      131 |        58 |       156 |          234 |                   452 |    0.71 |
| cenario     | ridge          | ICON                                    |   6 | 105 |       48 |        -2 |        64 |          102 |                   175 |    0.73 |
| cenario     | ridge          | ICON                                    |  12 | 105 |       88 |        28 |       106 |          164 |                   317 |    0.72 |
| cenario     | ridge          | ICON                                    |  18 | 102 |      116 |        94 |       146 |          229 |                   393 |    0.71 |
| cenario     | ridge          | ICON                                    |  24 |  93 |      122 |        99 |       148 |          209 |                   452 |    0.73 |
| cenario     | ridge          | sem mais chuva                          |   6 | 105 |       56 |       -21 |        75 |          117 |                   175 |    0.68 |
| cenario     | ridge          | sem mais chuva                          |  12 | 105 |      107 |       -24 |       131 |          219 |                   317 |    0.66 |
| cenario     | ridge          | sem mais chuva                          |  18 | 102 |      129 |       -13 |       154 |          235 |                   393 |    0.67 |
| cenario     | ridge          | sem mais chuva                          |  24 |  93 |      174 |       -39 |       204 |          319 |                   452 |    0.61 |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) |   6 |  70 |       59 |        -6 |        79 |          124 |                   198 |    0.7  |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) |  12 | 105 |       82 |         5 |       102 |          177 |                   317 |    0.74 |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) |  18 | 102 |       91 |        46 |       115 |          178 |                   393 |    0.77 |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) |  24 |  93 |       86 |        42 |       117 |          181 |                   452 |    0.81 |
| combinado   | combinado      | linear operacional                      |   3 |  84 |       22 |       -10 |        30 |           52 |                    80 |    0.72 |
| combinado   | combinado      | linear operacional                      |   6 |  37 |       35 |       -30 |        47 |           84 |                   138 |    0.74 |
| operacional | gbm_delta      | —                                       |   6 |  40 |       90 |       -32 |       109 |          158 |                   210 |    0.57 |
| operacional | gbm_delta      | —                                       |   9 |  79 |      119 |       -55 |       147 |          260 |                   278 |    0.57 |
| operacional | gbm_delta      | —                                       |  12 |  79 |      145 |       -90 |       185 |          310 |                   331 |    0.56 |
| operacional | linear         | —                                       |   3 |  88 |       22 |       -10 |        30 |           49 |                    82 |    0.73 |
| operacional | linear         | —                                       |   6 |  39 |       35 |       -28 |        46 |           82 |                   140 |    0.75 |
| operacional | linear         | —                                       |   9 |  39 |       67 |       -50 |        89 |          157 |                   217 |    0.69 |
| operacional | linear         | —                                       |  12 |  39 |      105 |       -66 |       133 |          234 |                   286 |    0.63 |
| operacional | ridge_montante | —                                       |   6 |  39 |       82 |       -31 |       101 |          167 |                   192 |    0.57 |

## Operacional × cenários nos mesmos pares

Mesma execução, alvo e validade. É a única comparação justa entre produtos; as tabelas gerais cobrem amostras diferentes.

| alvo      | motor_op       | cenario                                             |   n |   mae_operacional_cm |   mae_cenario_cm |
|:----------|:---------------|:----------------------------------------------------|----:|---------------------:|-----------------:|
| Encantado | gbm_delta      | combinado · cenários (média ridge+gbm, mediana NWP) |   9 |                  136 |               82 |
| Encantado | gbm_delta      | gbm · ECMWF                                         |   9 |                  136 |               96 |
| Encantado | gbm_delta      | gbm · GEM                                           |   9 |                  136 |              117 |
| Encantado | gbm_delta      | gbm · GFS                                           |   9 |                  136 |               86 |
| Encantado | gbm_delta      | gbm · ICON                                          |   9 |                  136 |               74 |
| Encantado | gbm_delta      | gbm · sem mais chuva                                |   9 |                  136 |              121 |
| Encantado | gbm_delta      | ridge · ECMWF                                       |   9 |                  136 |              129 |
| Encantado | gbm_delta      | ridge · GEM                                         |   9 |                  136 |              108 |
| Encantado | gbm_delta      | ridge · GFS                                         |   9 |                  136 |               88 |
| Encantado | gbm_delta      | ridge · ICON                                        |   9 |                  136 |               98 |
| Encantado | gbm_delta      | ridge · sem mais chuva                              |   9 |                  136 |              110 |
| Encantado | linear         | combinado · linear operacional                      |  36 |                   26 |               26 |
| Encantado | ridge_montante | combinado · cenários (média ridge+gbm, mediana NWP) |   9 |                  114 |               84 |
| Encantado | ridge_montante | gbm · ECMWF                                         |   9 |                  114 |              106 |
| Encantado | ridge_montante | gbm · GEM                                           |   9 |                  114 |              108 |
| Encantado | ridge_montante | gbm · GFS                                           |   9 |                  114 |               93 |
| Encantado | ridge_montante | gbm · ICON                                          |   9 |                  114 |               87 |
| Encantado | ridge_montante | gbm · sem mais chuva                                |   9 |                  114 |              108 |
| Encantado | ridge_montante | ridge · ECMWF                                       |   9 |                  114 |               88 |
| Encantado | ridge_montante | ridge · GEM                                         |   9 |                  114 |               84 |
| Encantado | ridge_montante | ridge · GFS                                         |   9 |                  114 |               79 |
| Encantado | ridge_montante | ridge · ICON                                        |   9 |                  114 |               73 |
| Encantado | ridge_montante | ridge · sem mais chuva                              |   9 |                  114 |               88 |
| Estrela   | linear         | combinado · cenários (média ridge+gbm, mediana NWP) |   9 |                  152 |               92 |
| Estrela   | linear         | combinado · linear operacional                      |  72 |                   25 |               25 |
| Estrela   | linear         | gbm · ECMWF                                         |  18 |                  108 |               79 |
| Estrela   | linear         | gbm · GEM                                           |  18 |                  108 |               67 |
| Estrela   | linear         | gbm · GFS                                           |  18 |                  108 |               57 |
| Estrela   | linear         | gbm · ICON                                          |  18 |                  108 |               54 |
| Estrela   | linear         | gbm · sem mais chuva                                |  18 |                  108 |               69 |
| Estrela   | linear         | ridge · ECMWF                                       |  18 |                  108 |               86 |
| Estrela   | linear         | ridge · GEM                                         |  18 |                  108 |               87 |
| Estrela   | linear         | ridge · GFS                                         |  18 |                  108 |               77 |
| Estrela   | linear         | ridge · ICON                                        |  18 |                  108 |               73 |
| Estrela   | linear         | ridge · sem mais chuva                              |  18 |                  108 |               89 |
| Muçum     | gbm_delta      | combinado · cenários (média ridge+gbm, mediana NWP) |  20 |                  155 |              133 |
| Muçum     | gbm_delta      | gbm · ECMWF                                         |  20 |                  155 |              140 |
| Muçum     | gbm_delta      | gbm · GEM                                           |  20 |                  155 |              161 |
| Muçum     | gbm_delta      | gbm · GFS                                           |  20 |                  155 |              140 |
| Muçum     | gbm_delta      | gbm · ICON                                          |  20 |                  155 |              129 |
| Muçum     | gbm_delta      | gbm · sem mais chuva                                |  20 |                  155 |              162 |
| Muçum     | gbm_delta      | ridge · ECMWF                                       |  20 |                  155 |              126 |
| Muçum     | gbm_delta      | ridge · GEM                                         |  20 |                  155 |              141 |
| Muçum     | gbm_delta      | ridge · GFS                                         |  20 |                  155 |              128 |
| Muçum     | gbm_delta      | ridge · ICON                                        |  20 |                  155 |              118 |
| Muçum     | gbm_delta      | ridge · sem mais chuva                              |  20 |                  155 |              149 |
| Muçum     | linear         | combinado · linear operacional                      |  10 |                   34 |               34 |

## Por fase da cheia

| produto     | motor          | cenario                                 | fase     |   n |   mae_cm |   vies_cm |   rmse_cm |   p90_abs_cm |   mae_persistencia_cm |   skill |
|:------------|:---------------|:----------------------------------------|:---------|----:|---------:|----------:|----------:|-------------:|----------------------:|--------:|
| cenario     | gbm            | ECMWF                                   | pico     |  51 |      152 |        55 |       172 |          271 |                   321 |    0.53 |
| cenario     | gbm            | ECMWF                                   | recessao | 186 |       75 |        16 |       107 |          161 |                   326 |    0.77 |
| cenario     | gbm            | ECMWF                                   | subida   | 168 |       99 |       -30 |       129 |          213 |                   339 |    0.71 |
| cenario     | gbm            | GEM                                     | pico     |  51 |      168 |        29 |       193 |          309 |                   321 |    0.48 |
| cenario     | gbm            | GEM                                     | recessao | 186 |       73 |        21 |       105 |          160 |                   326 |    0.78 |
| cenario     | gbm            | GEM                                     | subida   | 168 |      100 |       -27 |       126 |          212 |                   339 |    0.7  |
| cenario     | gbm            | GFS                                     | pico     |  51 |      178 |       -16 |       203 |          301 |                   321 |    0.45 |
| cenario     | gbm            | GFS                                     | recessao | 186 |       73 |        12 |       109 |          158 |                   326 |    0.78 |
| cenario     | gbm            | GFS                                     | subida   | 168 |      100 |       -57 |       128 |          225 |                   339 |    0.7  |
| cenario     | gbm            | ICON                                    | pico     |  51 |      171 |        56 |       193 |          280 |                   321 |    0.47 |
| cenario     | gbm            | ICON                                    | recessao | 186 |       75 |        11 |       107 |          162 |                   326 |    0.77 |
| cenario     | gbm            | ICON                                    | subida   | 168 |      114 |        27 |       151 |          251 |                   339 |    0.66 |
| cenario     | gbm            | sem mais chuva                          | pico     |  51 |      220 |       -65 |       256 |          368 |                   321 |    0.31 |
| cenario     | gbm            | sem mais chuva                          | recessao | 186 |       76 |         3 |       110 |          162 |                   326 |    0.77 |
| cenario     | gbm            | sem mais chuva                          | subida   | 168 |      158 |      -131 |       201 |          316 |                   339 |    0.53 |
| cenario     | ridge          | ECMWF                                   | pico     |  51 |       76 |        20 |        92 |          158 |                   321 |    0.76 |
| cenario     | ridge          | ECMWF                                   | recessao | 186 |      107 |        99 |       136 |          223 |                   326 |    0.67 |
| cenario     | ridge          | ECMWF                                   | subida   | 168 |       86 |       -15 |       116 |          196 |                   339 |    0.75 |
| cenario     | ridge          | GEM                                     | pico     |  51 |       67 |        24 |        81 |          135 |                   321 |    0.79 |
| cenario     | ridge          | GEM                                     | recessao | 186 |      118 |       112 |       147 |          229 |                   326 |    0.64 |
| cenario     | ridge          | GEM                                     | subida   | 168 |       86 |        -9 |       119 |          213 |                   339 |    0.74 |
| cenario     | ridge          | GFS                                     | pico     |  51 |       89 |       -41 |       111 |          182 |                   321 |    0.72 |
| cenario     | ridge          | GFS                                     | recessao | 186 |      112 |       102 |       139 |          232 |                   326 |    0.66 |
| cenario     | ridge          | GFS                                     | subida   | 168 |       83 |       -41 |       107 |          192 |                   339 |    0.76 |
| cenario     | ridge          | ICON                                    | pico     |  51 |       73 |        23 |        88 |          153 |                   321 |    0.77 |
| cenario     | ridge          | ICON                                    | recessao | 186 |      105 |        96 |       133 |          218 |                   326 |    0.68 |
| cenario     | ridge          | ICON                                    | subida   | 168 |       84 |        15 |       113 |          178 |                   339 |    0.75 |
| cenario     | ridge          | sem mais chuva                          | pico     |  51 |      139 |      -103 |       177 |          267 |                   321 |    0.57 |
| cenario     | ridge          | sem mais chuva                          | recessao | 186 |       96 |        73 |       121 |          196 |                   326 |    0.71 |
| cenario     | ridge          | sem mais chuva                          | subida   | 168 |      128 |      -107 |       162 |          275 |                   339 |    0.62 |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) | pico     |  51 |       92 |        22 |       113 |          183 |                   321 |    0.71 |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) | recessao | 175 |       71 |        61 |       101 |          159 |                   339 |    0.79 |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) | subida   | 144 |       90 |       -23 |       109 |          177 |                   373 |    0.76 |
| combinado   | combinado      | linear operacional                      | pico     |   1 |        7 |        -7 |         7 |            7 |                    74 |    0.91 |
| combinado   | combinado      | linear operacional                      | recessao |  34 |       12 |         6 |        14 |           22 |                    94 |    0.88 |
| combinado   | combinado      | linear operacional                      | subida   |  86 |       32 |       -25 |        42 |           67 |                   100 |    0.68 |
| operacional | gbm_delta      | —                                       | pico     |  36 |      144 |      -131 |       182 |          298 |                   255 |    0.44 |
| operacional | gbm_delta      | —                                       | recessao |  73 |       72 |        38 |       100 |          150 |                   271 |    0.74 |
| operacional | gbm_delta      | —                                       | subida   |  89 |      158 |      -121 |       183 |          281 |                   309 |    0.49 |
| operacional | linear         | —                                       | pico     |   9 |       22 |       -22 |        34 |           44 |                   128 |    0.83 |
| operacional | linear         | —                                       | recessao |  58 |       21 |        17 |        27 |           47 |                   158 |    0.87 |
| operacional | linear         | —                                       | subida   | 138 |       62 |       -53 |        90 |          160 |                   159 |    0.61 |
| operacional | ridge_montante | —                                       | pico     |   5 |       41 |       -34 |        64 |          100 |                   173 |    0.76 |
| operacional | ridge_montante | —                                       | recessao |  12 |       49 |        48 |        61 |           80 |                   198 |    0.75 |
| operacional | ridge_montante | —                                       | subida   |  22 |      109 |       -73 |       123 |          170 |                   194 |    0.44 |

## Por alvo (produto operacional e cenários)

| alvo      | produto     | motor          |   h |   n |   mae_cm |   vies_cm |   rmse_cm |   p90_abs_cm |   mae_persistencia_cm |   skill |
|:----------|:------------|:---------------|----:|----:|---------:|----------:|----------:|-------------:|----------------------:|--------:|
| Encantado | cenario     | gbm            |   6 | 175 |       61 |       -16 |        80 |          142 |                   190 |    0.68 |
| Encantado | cenario     | gbm            |  12 | 175 |      107 |        -9 |       131 |          211 |                   329 |    0.68 |
| Encantado | cenario     | gbm            |  18 | 170 |      127 |        25 |       169 |          318 |                   393 |    0.68 |
| Encantado | cenario     | gbm            |  24 | 155 |      142 |        23 |       192 |          358 |                   447 |    0.68 |
| Encantado | cenario     | ridge          |   6 | 175 |       49 |         1 |        62 |          112 |                   190 |    0.74 |
| Encantado | cenario     | ridge          |  12 | 175 |       98 |        41 |       116 |          173 |                   329 |    0.7  |
| Encantado | cenario     | ridge          |  18 | 170 |      131 |        94 |       161 |          236 |                   393 |    0.67 |
| Encantado | cenario     | ridge          |  24 | 155 |      153 |       100 |       181 |          273 |                   447 |    0.66 |
| Encantado | combinado   | combinado      |   3 |  37 |       26 |       -11 |        32 |           56 |                    96 |    0.73 |
| Encantado | combinado   | combinado      |   6 |  35 |       45 |        -5 |        61 |          106 |                   190 |    0.76 |
| Encantado | combinado   | combinado      |  12 |  35 |       80 |        23 |        95 |          155 |                   329 |    0.76 |
| Encantado | combinado   | combinado      |  18 |  34 |       98 |        78 |       128 |          237 |                   393 |    0.75 |
| Encantado | combinado   | combinado      |  24 |  31 |       96 |        89 |       139 |          296 |                   447 |    0.79 |
| Encantado | operacional | gbm_delta      |   9 |  39 |      107 |       -40 |       130 |          241 |                   270 |    0.61 |
| Encantado | operacional | gbm_delta      |  12 |  39 |      126 |       -77 |       165 |          295 |                   324 |    0.61 |
| Encantado | operacional | linear         |   3 |  39 |       26 |       -11 |        32 |           56 |                    97 |    0.73 |
| Encantado | operacional | ridge_montante |   6 |  39 |       82 |       -31 |       101 |          167 |                   192 |    0.57 |
| Estrela   | cenario     | gbm            |   6 | 175 |       25 |         8 |        32 |           48 |                   129 |    0.81 |
| Estrela   | cenario     | gbm            |  12 | 175 |       86 |        16 |       112 |          192 |                   281 |    0.69 |
| Estrela   | cenario     | gbm            |  18 | 170 |      111 |        34 |       140 |          246 |                   389 |    0.71 |
| Estrela   | cenario     | gbm            |  24 | 155 |      106 |       -10 |       135 |          247 |                   465 |    0.77 |
| Estrela   | cenario     | ridge          |   6 | 175 |       32 |       -22 |        41 |           81 |                   129 |    0.75 |
| Estrela   | cenario     | ridge          |  12 | 175 |       66 |       -35 |        87 |          162 |                   281 |    0.77 |
| Estrela   | cenario     | ridge          |  18 | 170 |       90 |         1 |       111 |          177 |                   389 |    0.77 |
| Estrela   | cenario     | ridge          |  24 | 155 |       98 |        16 |       120 |          188 |                   465 |    0.79 |
| Estrela   | combinado   | combinado      |   3 |  37 |       16 |       -12 |        20 |           35 |                    64 |    0.75 |
| Estrela   | combinado   | combinado      |   6 |  37 |       35 |       -30 |        47 |           84 |                   138 |    0.74 |
| Estrela   | combinado   | combinado      |  12 |  35 |       60 |        -5 |        78 |          127 |                   281 |    0.79 |
| Estrela   | combinado   | combinado      |  18 |  34 |       84 |        30 |        99 |          152 |                   389 |    0.78 |
| Estrela   | combinado   | combinado      |  24 |  31 |       79 |        26 |        88 |          132 |                   465 |    0.83 |
| Estrela   | operacional | linear         |   3 |  39 |       15 |       -11 |        20 |           35 |                    66 |    0.77 |
| Estrela   | operacional | linear         |   6 |  39 |       35 |       -28 |        46 |           82 |                   140 |    0.75 |
| Estrela   | operacional | linear         |   9 |  39 |       67 |       -50 |        89 |          157 |                   217 |    0.69 |
| Estrela   | operacional | linear         |  12 |  39 |      105 |       -66 |       133 |          234 |                   286 |    0.63 |
| Muçum     | cenario     | gbm            |   6 | 175 |       82 |       -13 |       108 |          170 |                   206 |    0.6  |
| Muçum     | cenario     | gbm            |  12 | 175 |      130 |       -47 |       162 |          257 |                   342 |    0.62 |
| Muçum     | cenario     | gbm            |  18 | 170 |      126 |       -51 |       162 |          284 |                   397 |    0.68 |
| Muçum     | cenario     | gbm            |  24 | 155 |      157 |       -93 |       199 |          344 |                   445 |    0.65 |
| Muçum     | cenario     | ridge          |   6 | 175 |       72 |        -7 |        93 |          163 |                   206 |    0.65 |
| Muçum     | cenario     | ridge          |  12 | 175 |      124 |        28 |       143 |          215 |                   342 |    0.64 |
| Muçum     | cenario     | ridge          |  18 | 170 |      137 |        78 |       163 |          249 |                   397 |    0.66 |
| Muçum     | cenario     | ridge          |  24 | 155 |      158 |        68 |       189 |          303 |                   445 |    0.65 |
| Muçum     | combinado   | combinado      |   3 |  10 |       34 |        -2 |        47 |           69 |                    86 |    0.61 |
| Muçum     | combinado   | combinado      |   6 |  35 |       73 |        -8 |        93 |          140 |                   206 |    0.65 |
| Muçum     | combinado   | combinado      |  12 |  35 |      107 |        -3 |       127 |          212 |                   342 |    0.69 |
| Muçum     | combinado   | combinado      |  18 |  34 |       91 |        29 |       115 |          177 |                   397 |    0.77 |
| Muçum     | combinado   | combinado      |  24 |  31 |       82 |        10 |       119 |          213 |                   445 |    0.82 |
| Muçum     | operacional | gbm_delta      |   6 |  40 |       90 |       -32 |       109 |          158 |                   210 |    0.57 |
| Muçum     | operacional | gbm_delta      |   9 |  40 |      131 |       -69 |       161 |          275 |                   286 |    0.54 |
| Muçum     | operacional | gbm_delta      |  12 |  40 |      164 |      -102 |       203 |          312 |                   338 |    0.52 |
| Muçum     | operacional | linear         |   3 |  10 |       34 |        -2 |        47 |           69 |                    86 |    0.61 |

## Por evento

| evento     | produto     |   h |   n |   mae_cm |   vies_cm |   rmse_cm |   p90_abs_cm |   mae_persistencia_cm |   skill |
|:-----------|:------------|----:|----:|---------:|----------:|----------:|-------------:|----------------------:|--------:|
| 2026-09-21 | operacional |   3 |   4 |       21 |         2 |        25 |           34 |                   114 |    0.81 |
| 2026-09-21 | operacional |   6 |   6 |      120 |        -9 |       142 |          198 |                   257 |    0.53 |
| 2026-09-21 | operacional |   9 |   6 |      179 |        -8 |       210 |          278 |                   328 |    0.45 |
| 2026-09-21 | operacional |  12 |   6 |      218 |         2 |       248 |          323 |                   355 |    0.39 |
| 2026-09-28 | cenario     |   6 | 900 |       56 |       -10 |        78 |          134 |                   195 |    0.71 |
| 2026-09-28 | cenario     |  12 | 900 |      105 |         0 |       131 |          222 |                   332 |    0.68 |
| 2026-09-28 | cenario     |  18 | 900 |      119 |        37 |       150 |          248 |                   391 |    0.7  |
| 2026-09-28 | cenario     |  24 | 900 |      134 |        20 |       169 |          291 |                   450 |    0.7  |
| 2026-09-28 | combinado   |   3 |  67 |       23 |       -11 |        31 |           55 |                    94 |    0.75 |
| 2026-09-28 | combinado   |   6 |  91 |       54 |       -17 |        73 |          120 |                   199 |    0.73 |
| 2026-09-28 | combinado   |  12 |  90 |       85 |         5 |       106 |          185 |                   332 |    0.74 |
| 2026-09-28 | combinado   |  18 |  90 |       95 |        49 |       119 |          196 |                   391 |    0.76 |
| 2026-09-28 | combinado   |  24 |  90 |       87 |        42 |       119 |          185 |                   450 |    0.81 |
| 2026-09-28 | operacional |   3 |  67 |       23 |       -11 |        31 |           55 |                    94 |    0.75 |
| 2026-09-28 | operacional |   6 |  94 |       70 |       -30 |        90 |          146 |                   196 |    0.64 |
| 2026-09-28 | operacional |   9 |  94 |      101 |       -51 |       130 |          201 |                   271 |    0.63 |
| 2026-09-28 | operacional |  12 |  94 |      125 |       -76 |       167 |          278 |                   322 |    0.61 |
| 2026-11-04 | cenario     |   6 | 150 |       38 |         7 |        51 |           87 |                    56 |    0.32 |
| 2026-11-04 | cenario     |  12 | 150 |       84 |        -8 |       103 |          166 |                   230 |    0.64 |
| 2026-11-04 | cenario     |  18 | 120 |      129 |       -22 |       166 |          282 |                   412 |    0.69 |
| 2026-11-04 | cenario     |  24 |  30 |      189 |       -70 |       240 |          423 |                   508 |    0.63 |
| 2026-11-04 | combinado   |   3 |  17 |       18 |        -8 |        24 |           38 |                    25 |    0.29 |
| 2026-11-04 | combinado   |   6 |  16 |       33 |        -1 |        47 |           79 |                    57 |    0.42 |
| 2026-11-04 | combinado   |  12 |  15 |       66 |         5 |        75 |          104 |                   230 |    0.72 |
| 2026-11-04 | combinado   |  18 |  12 |       62 |        23 |        81 |          120 |                   412 |    0.85 |
| 2026-11-04 | combinado   |  24 |   3 |       59 |        19 |        61 |           75 |                   508 |    0.88 |
| 2026-11-04 | operacional |   3 |  17 |       18 |        -8 |        24 |           38 |                    25 |    0.29 |
| 2026-11-04 | operacional |   6 |  18 |       48 |       -39 |        67 |          111 |                    75 |    0.36 |
| 2026-11-04 | operacional |   9 |  18 |       81 |       -81 |        96 |          149 |                   167 |    0.51 |
| 2026-11-04 | operacional |  12 |  18 |      140 |      -140 |       153 |          207 |                   271 |    0.48 |
