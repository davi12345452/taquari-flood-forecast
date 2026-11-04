# Placar das emissões reais

Gerado em 04/11/2026 11:41 (UTC−3) por `src/live/placar.py`. 4399 pares previsto × observado de 36 emissões, em 2 eventos. Só entram números gravados antes da observação; replays não contam. Reexecuções com a mesma referência contam uma vez (a primeira).

`skill` = 1 − MAE/MAE da persistência nos mesmos pares: 1 é perfeito, 0 empata com repetir a cota atual, negativo é pior. `fase` é relativa ao máximo observado do alvo no evento (pico = ±3h).

## Por produto, motor e horizonte

| produto     | motor          | cenario                                 |   h |   n |   mae_cm |   vies_cm |   rmse_cm |   p90_abs_cm |   mae_persistencia_cm |   skill |
|:------------|:---------------|:----------------------------------------|----:|----:|---------:|----------:|----------:|-------------:|----------------------:|--------:|
| cenario     | gbm            | ECMWF                                   |   6 |  90 |       59 |        -9 |        84 |          146 |                   195 |    0.7  |
| cenario     | gbm            | ECMWF                                   |  12 |  90 |      110 |        -9 |       140 |          252 |                   332 |    0.67 |
| cenario     | gbm            | ECMWF                                   |  18 |  90 |      110 |        18 |       140 |          250 |                   391 |    0.72 |
| cenario     | gbm            | ECMWF                                   |  24 |  90 |      108 |       -20 |       142 |          215 |                   450 |    0.76 |
| cenario     | gbm            | GEM                                     |   6 |  90 |       57 |        -6 |        83 |          147 |                   195 |    0.71 |
| cenario     | gbm            | GEM                                     |  12 |  90 |      106 |        -8 |       135 |          247 |                   332 |    0.68 |
| cenario     | gbm            | GEM                                     |  18 |  90 |      110 |        17 |       141 |          245 |                   391 |    0.72 |
| cenario     | gbm            | GEM                                     |  24 |  90 |      106 |        15 |       135 |          222 |                   450 |    0.76 |
| cenario     | gbm            | GFS                                     |   6 |  90 |       59 |        -9 |        82 |          144 |                   195 |    0.7  |
| cenario     | gbm            | GFS                                     |  12 |  90 |      107 |       -14 |       137 |          240 |                   332 |    0.68 |
| cenario     | gbm            | GFS                                     |  18 |  90 |      107 |        -5 |       142 |          253 |                   391 |    0.73 |
| cenario     | gbm            | GFS                                     |  24 |  90 |      123 |       -32 |       160 |          287 |                   450 |    0.73 |
| cenario     | gbm            | ICON                                    |   6 |  90 |       54 |        -2 |        75 |          135 |                   195 |    0.72 |
| cenario     | gbm            | ICON                                    |  12 |  90 |       97 |         3 |       124 |          216 |                   332 |    0.71 |
| cenario     | gbm            | ICON                                    |  18 |  90 |      118 |        54 |       157 |          273 |                   391 |    0.7  |
| cenario     | gbm            | ICON                                    |  24 |  90 |      137 |        24 |       175 |          309 |                   450 |    0.7  |
| cenario     | gbm            | sem mais chuva                          |   6 |  90 |       63 |       -14 |        88 |          156 |                   195 |    0.68 |
| cenario     | gbm            | sem mais chuva                          |  12 |  90 |      119 |       -30 |       154 |          267 |                   332 |    0.64 |
| cenario     | gbm            | sem mais chuva                          |  18 |  90 |      129 |       -36 |       166 |          296 |                   391 |    0.67 |
| cenario     | gbm            | sem mais chuva                          |  24 |  90 |      184 |      -115 |       234 |          387 |                   450 |    0.59 |
| cenario     | ridge          | ECMWF                                   |   6 |  90 |       54 |       -13 |        72 |          114 |                   195 |    0.72 |
| cenario     | ridge          | ECMWF                                   |  12 |  90 |      100 |        19 |       124 |          184 |                   332 |    0.7  |
| cenario     | ridge          | ECMWF                                   |  18 |  90 |      118 |        80 |       149 |          236 |                   391 |    0.7  |
| cenario     | ridge          | ECMWF                                   |  24 |  90 |      123 |        82 |       152 |          218 |                   450 |    0.73 |
| cenario     | ridge          | GEM                                     |   6 |  90 |       52 |        -8 |        71 |          114 |                   195 |    0.73 |
| cenario     | ridge          | GEM                                     |  12 |  90 |       99 |        23 |       118 |          184 |                   332 |    0.7  |
| cenario     | ridge          | GEM                                     |  18 |  90 |      129 |        89 |       160 |          242 |                   391 |    0.67 |
| cenario     | ridge          | GEM                                     |  24 |  90 |      133 |       113 |       166 |          248 |                   450 |    0.7  |
| cenario     | ridge          | GFS                                     |   6 |  90 |       55 |       -13 |        72 |          110 |                   195 |    0.72 |
| cenario     | ridge          | GFS                                     |  12 |  90 |      106 |        10 |       125 |          199 |                   332 |    0.68 |
| cenario     | ridge          | GFS                                     |  18 |  90 |      123 |        54 |       145 |          240 |                   391 |    0.68 |
| cenario     | ridge          | GFS                                     |  24 |  90 |      131 |        64 |       156 |          234 |                   450 |    0.71 |
| cenario     | ridge          | ICON                                    |   6 |  90 |       48 |        -8 |        65 |          103 |                   195 |    0.76 |
| cenario     | ridge          | ICON                                    |  12 |  90 |       89 |        25 |       108 |          165 |                   332 |    0.73 |
| cenario     | ridge          | ICON                                    |  18 |  90 |      119 |        95 |       150 |          230 |                   391 |    0.69 |
| cenario     | ridge          | ICON                                    |  24 |  90 |      124 |       100 |       150 |          210 |                   450 |    0.73 |
| cenario     | ridge          | sem mais chuva                          |   6 |  90 |       61 |       -23 |        80 |          133 |                   195 |    0.69 |
| cenario     | ridge          | sem mais chuva                          |  12 |  90 |      113 |       -16 |       138 |          224 |                   332 |    0.66 |
| cenario     | ridge          | sem mais chuva                          |  18 |  90 |      127 |         5 |       151 |          226 |                   391 |    0.68 |
| cenario     | ridge          | sem mais chuva                          |  24 |  90 |      169 |       -29 |       197 |          303 |                   450 |    0.62 |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) |   6 |  60 |       62 |        -9 |        82 |          128 |                   221 |    0.72 |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) |  12 |  90 |       85 |         5 |       106 |          185 |                   332 |    0.74 |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) |  18 |  90 |       95 |        49 |       119 |          196 |                   391 |    0.76 |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) |  24 |  90 |       87 |        42 |       119 |          185 |                   450 |    0.81 |
| combinado   | combinado      | linear operacional                      |   3 |  67 |       23 |       -11 |        31 |           55 |                    94 |    0.75 |
| combinado   | combinado      | linear operacional                      |   6 |  31 |       39 |       -34 |        50 |           91 |                   156 |    0.75 |
| operacional | gbm_delta      | —                                       |   6 |  34 |       92 |       -27 |       112 |          153 |                   227 |    0.59 |
| operacional | gbm_delta      | —                                       |   9 |  67 |      123 |       -47 |       152 |          266 |                   292 |    0.58 |
| operacional | gbm_delta      | —                                       |  12 |  67 |      142 |       -76 |       187 |          320 |                   330 |    0.57 |
| operacional | linear         | —                                       |   3 |  71 |       23 |       -10 |        31 |           54 |                    95 |    0.76 |
| operacional | linear         | —                                       |   6 |  33 |       38 |       -31 |        49 |           88 |                   157 |    0.76 |
| operacional | linear         | —                                       |   9 |  33 |       70 |       -51 |        94 |          174 |                   240 |    0.71 |
| operacional | linear         | —                                       |  12 |  33 |      108 |       -62 |       139 |          235 |                   311 |    0.65 |
| operacional | ridge_montante | —                                       |   6 |  33 |       88 |       -28 |       106 |          169 |                   215 |    0.59 |

## Operacional × cenários nos mesmos pares

Mesma execução, alvo e validade. É a única comparação justa entre produtos; as tabelas gerais cobrem amostras diferentes.

| alvo      | motor_op       | cenario                                             |   n |   mae_operacional_cm |   mae_cenario_cm |
|:----------|:---------------|:----------------------------------------------------|----:|---------------------:|-----------------:|
| Encantado | gbm_delta      | combinado · cenários (média ridge+gbm, mediana NWP) |   7 |                  144 |               83 |
| Encantado | gbm_delta      | gbm · ECMWF                                         |   7 |                  144 |               94 |
| Encantado | gbm_delta      | gbm · GEM                                           |   7 |                  144 |              101 |
| Encantado | gbm_delta      | gbm · GFS                                           |   7 |                  144 |               74 |
| Encantado | gbm_delta      | gbm · ICON                                          |   7 |                  144 |               55 |
| Encantado | gbm_delta      | gbm · sem mais chuva                                |   7 |                  144 |              108 |
| Encantado | gbm_delta      | ridge · ECMWF                                       |   7 |                  144 |              143 |
| Encantado | gbm_delta      | ridge · GEM                                         |   7 |                  144 |              121 |
| Encantado | gbm_delta      | ridge · GFS                                         |   7 |                  144 |              103 |
| Encantado | gbm_delta      | ridge · ICON                                        |   7 |                  144 |              113 |
| Encantado | gbm_delta      | ridge · sem mais chuva                              |   7 |                  144 |              117 |
| Encantado | linear         | combinado · linear operacional                      |  30 |                   28 |               28 |
| Encantado | ridge_montante | combinado · cenários (média ridge+gbm, mediana NWP) |   7 |                  135 |              104 |
| Encantado | ridge_montante | gbm · ECMWF                                         |   7 |                  135 |              125 |
| Encantado | ridge_montante | gbm · GEM                                           |   7 |                  135 |              126 |
| Encantado | ridge_montante | gbm · GFS                                           |   7 |                  135 |              113 |
| Encantado | ridge_montante | gbm · ICON                                          |   7 |                  135 |              104 |
| Encantado | ridge_montante | gbm · sem mais chuva                                |   7 |                  135 |              125 |
| Encantado | ridge_montante | ridge · ECMWF                                       |   7 |                  135 |              103 |
| Encantado | ridge_montante | ridge · GEM                                         |   7 |                  135 |              106 |
| Encantado | ridge_montante | ridge · GFS                                         |   7 |                  135 |               99 |
| Encantado | ridge_montante | ridge · ICON                                        |   7 |                  135 |               90 |
| Encantado | ridge_montante | ridge · sem mais chuva                              |   7 |                  135 |              110 |
| Estrela   | linear         | combinado · cenários (média ridge+gbm, mediana NWP) |   7 |                  166 |              114 |
| Estrela   | linear         | combinado · linear operacional                      |  60 |                   26 |               26 |
| Estrela   | linear         | gbm · ECMWF                                         |  14 |                  122 |               79 |
| Estrela   | linear         | gbm · GEM                                           |  14 |                  122 |               80 |
| Estrela   | linear         | gbm · GFS                                           |  14 |                  122 |               71 |
| Estrela   | linear         | gbm · ICON                                          |  14 |                  122 |               65 |
| Estrela   | linear         | gbm · sem mais chuva                                |  14 |                  122 |               81 |
| Estrela   | linear         | ridge · ECMWF                                       |  14 |                  122 |              104 |
| Estrela   | linear         | ridge · GEM                                         |  14 |                  122 |              106 |
| Estrela   | linear         | ridge · GFS                                         |  14 |                  122 |               94 |
| Estrela   | linear         | ridge · ICON                                        |  14 |                  122 |               90 |
| Estrela   | linear         | ridge · sem mais chuva                              |  14 |                  122 |              108 |
| Muçum     | gbm_delta      | combinado · cenários (média ridge+gbm, mediana NWP) |  16 |                  162 |              140 |
| Muçum     | gbm_delta      | gbm · ECMWF                                         |  16 |                  162 |              158 |
| Muçum     | gbm_delta      | gbm · GEM                                           |  16 |                  162 |              159 |
| Muçum     | gbm_delta      | gbm · GFS                                           |  16 |                  162 |              143 |
| Muçum     | gbm_delta      | gbm · ICON                                          |  16 |                  162 |              125 |
| Muçum     | gbm_delta      | gbm · sem mais chuva                                |  16 |                  162 |              158 |
| Muçum     | gbm_delta      | ridge · ECMWF                                       |  16 |                  162 |              150 |
| Muçum     | gbm_delta      | ridge · GEM                                         |  16 |                  162 |              152 |
| Muçum     | gbm_delta      | ridge · GFS                                         |  16 |                  162 |              142 |
| Muçum     | gbm_delta      | ridge · ICON                                        |  16 |                  162 |              132 |
| Muçum     | gbm_delta      | ridge · sem mais chuva                              |  16 |                  162 |              157 |
| Muçum     | linear         | combinado · linear operacional                      |   5 |                   48 |               48 |

## Por fase da cheia

| produto     | motor          | cenario                                 | fase     |   n |   mae_cm |   vies_cm |   rmse_cm |   p90_abs_cm |   mae_persistencia_cm |   skill |
|:------------|:---------------|:----------------------------------------|:---------|----:|---------:|----------:|----------:|-------------:|----------------------:|--------:|
| cenario     | gbm            | ECMWF                                   | pico     |  39 |      163 |        54 |       181 |          276 |                   279 |    0.42 |
| cenario     | gbm            | ECMWF                                   | recessao | 186 |       75 |        16 |       107 |          161 |                   326 |    0.77 |
| cenario     | gbm            | ECMWF                                   | subida   | 135 |      107 |       -52 |       138 |          248 |                   383 |    0.72 |
| cenario     | gbm            | GEM                                     | pico     |  39 |      167 |        53 |       186 |          271 |                   279 |    0.4  |
| cenario     | gbm            | GEM                                     | recessao | 186 |       73 |        21 |       105 |          160 |                   326 |    0.78 |
| cenario     | gbm            | GEM                                     | subida   | 135 |      104 |       -32 |       129 |          214 |                   383 |    0.73 |
| cenario     | gbm            | GFS                                     | pico     |  39 |      181 |        24 |       206 |          301 |                   279 |    0.35 |
| cenario     | gbm            | GFS                                     | recessao | 186 |       73 |        12 |       109 |          158 |                   326 |    0.78 |
| cenario     | gbm            | GFS                                     | subida   | 135 |      111 |       -64 |       138 |          232 |                   383 |    0.71 |
| cenario     | gbm            | ICON                                    | pico     |  39 |      169 |        47 |       189 |          281 |                   279 |    0.39 |
| cenario     | gbm            | ICON                                    | recessao | 186 |       75 |        11 |       107 |          162 |                   326 |    0.77 |
| cenario     | gbm            | ICON                                    | subida   | 135 |      118 |        24 |       157 |          259 |                   383 |    0.69 |
| cenario     | gbm            | sem mais chuva                          | pico     |  39 |      189 |        14 |       218 |          329 |                   279 |    0.32 |
| cenario     | gbm            | sem mais chuva                          | recessao | 186 |       76 |         3 |       110 |          162 |                   326 |    0.77 |
| cenario     | gbm            | sem mais chuva                          | subida   | 135 |      170 |      -138 |       213 |          346 |                   383 |    0.55 |
| cenario     | ridge          | ECMWF                                   | pico     |  39 |       69 |         6 |        83 |          137 |                   279 |    0.75 |
| cenario     | ridge          | ECMWF                                   | recessao | 186 |      107 |        99 |       136 |          223 |                   326 |    0.67 |
| cenario     | ridge          | ECMWF                                   | subida   | 135 |       97 |       -26 |       128 |          222 |                   383 |    0.75 |
| cenario     | ridge          | GEM                                     | pico     |  39 |       68 |        27 |        82 |          123 |                   279 |    0.76 |
| cenario     | ridge          | GEM                                     | recessao | 186 |      118 |       112 |       147 |          229 |                   326 |    0.64 |
| cenario     | ridge          | GEM                                     | subida   | 135 |       94 |       -17 |       128 |          230 |                   383 |    0.76 |
| cenario     | ridge          | GFS                                     | pico     |  39 |       96 |       -44 |       117 |          183 |                   279 |    0.65 |
| cenario     | ridge          | GFS                                     | recessao | 186 |      112 |       102 |       139 |          232 |                   326 |    0.66 |
| cenario     | ridge          | GFS                                     | subida   | 135 |       94 |       -51 |       117 |          203 |                   383 |    0.75 |
| cenario     | ridge          | ICON                                    | pico     |  39 |       69 |         4 |        82 |          127 |                   279 |    0.75 |
| cenario     | ridge          | ICON                                    | recessao | 186 |      105 |        96 |       133 |          218 |                   326 |    0.68 |
| cenario     | ridge          | ICON                                    | subida   | 135 |       88 |         8 |       119 |          187 |                   383 |    0.77 |
| cenario     | ridge          | sem mais chuva                          | pico     |  39 |      126 |       -78 |       159 |          265 |                   279 |    0.55 |
| cenario     | ridge          | sem mais chuva                          | recessao | 186 |       96 |        73 |       121 |          196 |                   326 |    0.71 |
| cenario     | ridge          | sem mais chuva                          | subida   | 135 |      145 |      -120 |       175 |          287 |                   383 |    0.62 |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) | pico     |  39 |      103 |        26 |       122 |          198 |                   279 |    0.63 |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) | recessao | 175 |       71 |        61 |       101 |          159 |                   339 |    0.79 |
| combinado   | combinado      | cenários (média ridge+gbm, mediana NWP) | subida   | 116 |       97 |       -32 |       117 |          181 |                   419 |    0.77 |
| combinado   | combinado      | linear operacional                      | pico     |   1 |        7 |        -7 |         7 |            7 |                    74 |    0.91 |
| combinado   | combinado      | linear operacional                      | recessao |  34 |       12 |         6 |        14 |           22 |                    94 |    0.88 |
| combinado   | combinado      | linear operacional                      | subida   |  63 |       38 |       -31 |        47 |           75 |                   125 |    0.7  |
| operacional | gbm_delta      | —                                       | pico     |  36 |      144 |      -131 |       182 |          298 |                   255 |    0.44 |
| operacional | gbm_delta      | —                                       | recessao |  73 |       72 |        38 |       100 |          150 |                   271 |    0.74 |
| operacional | gbm_delta      | —                                       | subida   |  59 |      177 |      -123 |       202 |          290 |                   346 |    0.49 |
| operacional | linear         | —                                       | pico     |   9 |       22 |       -22 |        34 |           44 |                   128 |    0.83 |
| operacional | linear         | —                                       | recessao |  58 |       21 |        17 |        27 |           47 |                   158 |    0.87 |
| operacional | linear         | —                                       | subida   | 103 |       72 |       -61 |       100 |          193 |                   192 |    0.63 |
| operacional | ridge_montante | —                                       | pico     |   5 |       41 |       -34 |        64 |          100 |                   173 |    0.76 |
| operacional | ridge_montante | —                                       | recessao |  12 |       49 |        48 |        61 |           80 |                   198 |    0.75 |
| operacional | ridge_montante | —                                       | subida   |  16 |      131 |       -82 |       139 |          179 |                   241 |    0.46 |

## Por alvo (produto operacional e cenários)

| alvo      | produto     | motor          |   h |   n |   mae_cm |   vies_cm |   rmse_cm |   p90_abs_cm |   mae_persistencia_cm |   skill |
|:----------|:------------|:---------------|----:|----:|---------:|----------:|----------:|-------------:|----------------------:|--------:|
| Encantado | cenario     | gbm            |   6 | 150 |       66 |       -18 |        85 |          144 |                   212 |    0.69 |
| Encantado | cenario     | gbm            |  12 | 150 |      106 |        -4 |       132 |          234 |                   343 |    0.69 |
| Encantado | cenario     | gbm            |  18 | 150 |      121 |        43 |       162 |          298 |                   385 |    0.69 |
| Encantado | cenario     | gbm            |  24 | 150 |      139 |        29 |       187 |          358 |                   442 |    0.69 |
| Encantado | cenario     | ridge          |   6 | 150 |       53 |        -0 |        65 |          115 |                   212 |    0.75 |
| Encantado | cenario     | ridge          |  12 | 150 |      104 |        47 |       122 |          182 |                   343 |    0.7  |
| Encantado | cenario     | ridge          |  18 | 150 |      136 |       109 |       166 |          238 |                   385 |    0.65 |
| Encantado | cenario     | ridge          |  24 | 150 |      152 |       108 |       179 |          271 |                   442 |    0.66 |
| Encantado | combinado   | combinado      |   3 |  31 |       28 |       -12 |        34 |           56 |                   111 |    0.75 |
| Encantado | combinado   | combinado      |   6 |  30 |       49 |        -7 |        65 |          120 |                   212 |    0.77 |
| Encantado | combinado   | combinado      |  12 |  30 |       83 |        26 |        99 |          159 |                   343 |    0.76 |
| Encantado | combinado   | combinado      |  18 |  30 |      105 |        90 |       135 |          242 |                   385 |    0.73 |
| Encantado | combinado   | combinado      |  24 |  30 |       97 |        94 |       141 |          296 |                   442 |    0.78 |
| Encantado | operacional | gbm_delta      |   9 |  33 |      111 |       -32 |       137 |          245 |                   289 |    0.62 |
| Encantado | operacional | gbm_delta      |  12 |  33 |      124 |       -65 |       169 |          307 |                   332 |    0.63 |
| Encantado | operacional | linear         |   3 |  33 |       28 |       -11 |        34 |           56 |                   111 |    0.74 |
| Encantado | operacional | ridge_montante |   6 |  33 |       88 |       -28 |       106 |          169 |                   215 |    0.59 |
| Estrela   | cenario     | gbm            |   6 | 150 |       26 |         8 |        33 |           48 |                   144 |    0.82 |
| Estrela   | cenario     | gbm            |  12 | 150 |       91 |        15 |       118 |          192 |                   306 |    0.7  |
| Estrela   | cenario     | gbm            |  18 | 150 |      109 |        30 |       139 |          246 |                   410 |    0.73 |
| Estrela   | cenario     | gbm            |  24 | 150 |      105 |       -12 |       133 |          241 |                   470 |    0.78 |
| Estrela   | cenario     | ridge          |   6 | 150 |       33 |       -28 |        43 |           84 |                   144 |    0.77 |
| Estrela   | cenario     | ridge          |  12 | 150 |       71 |       -44 |        92 |          168 |                   306 |    0.77 |
| Estrela   | cenario     | ridge          |  18 | 150 |       94 |        -5 |       115 |          189 |                   410 |    0.77 |
| Estrela   | cenario     | ridge          |  24 | 150 |       99 |        16 |       121 |          189 |                   470 |    0.79 |
| Estrela   | combinado   | combinado      |   3 |  31 |       15 |       -12 |        20 |           27 |                    70 |    0.79 |
| Estrela   | combinado   | combinado      |   6 |  31 |       39 |       -34 |        50 |           91 |                   156 |    0.75 |
| Estrela   | combinado   | combinado      |  12 |  30 |       64 |       -10 |        82 |          131 |                   306 |    0.79 |
| Estrela   | combinado   | combinado      |  18 |  30 |       84 |        23 |        99 |          156 |                   410 |    0.8  |
| Estrela   | combinado   | combinado      |  24 |  30 |       79 |        25 |        89 |          132 |                   470 |    0.83 |
| Estrela   | operacional | linear         |   3 |  33 |       14 |       -11 |        19 |           27 |                    73 |    0.8  |
| Estrela   | operacional | linear         |   6 |  33 |       38 |       -31 |        49 |           88 |                   157 |    0.76 |
| Estrela   | operacional | linear         |   9 |  33 |       70 |       -51 |        94 |          174 |                   240 |    0.71 |
| Estrela   | operacional | linear         |  12 |  33 |      108 |       -62 |       139 |          235 |                   311 |    0.65 |
| Muçum     | cenario     | gbm            |   6 | 150 |       83 |       -14 |       111 |          178 |                   229 |    0.64 |
| Muçum     | cenario     | gbm            |  12 | 150 |      126 |       -46 |       162 |          259 |                   345 |    0.64 |
| Muçum     | cenario     | gbm            |  18 | 150 |      114 |       -44 |       146 |          250 |                   376 |    0.7  |
| Muçum     | cenario     | gbm            |  24 | 150 |      152 |       -94 |       192 |          329 |                   439 |    0.65 |
| Muçum     | cenario     | ridge          |   6 | 150 |       75 |       -10 |        98 |          177 |                   229 |    0.67 |
| Muçum     | cenario     | ridge          |  12 | 150 |      129 |        34 |       148 |          236 |                   345 |    0.63 |
| Muçum     | cenario     | ridge          |  18 | 150 |      140 |        91 |       166 |          250 |                   376 |    0.63 |
| Muçum     | cenario     | ridge          |  24 | 150 |      157 |        74 |       188 |          301 |                   439 |    0.64 |
| Muçum     | combinado   | combinado      |   3 |   5 |       48 |         4 |        59 |           87 |                   142 |    0.66 |
| Muçum     | combinado   | combinado      |   6 |  30 |       74 |       -10 |        96 |          151 |                   229 |    0.68 |
| Muçum     | combinado   | combinado      |  12 |  30 |      109 |        -2 |       131 |          215 |                   345 |    0.69 |
| Muçum     | combinado   | combinado      |  18 |  30 |       95 |        33 |       119 |          184 |                   376 |    0.75 |
| Muçum     | combinado   | combinado      |  24 |  30 |       84 |         9 |       121 |          215 |                   439 |    0.81 |
| Muçum     | operacional | gbm_delta      |   6 |  34 |       92 |       -27 |       112 |          153 |                   227 |    0.59 |
| Muçum     | operacional | gbm_delta      |   9 |  34 |      134 |       -61 |       166 |          281 |                   294 |    0.54 |
| Muçum     | operacional | gbm_delta      |  12 |  34 |      158 |       -86 |       203 |          326 |                   328 |    0.52 |
| Muçum     | operacional | linear         |   3 |   5 |       48 |         4 |        59 |           87 |                   142 |    0.66 |

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
