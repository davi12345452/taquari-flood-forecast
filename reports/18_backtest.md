# Backtest fora da amostra: cenários de chuva e produto combinado

Eventos: ev20240430, ev20240616, ev20241012, ev20250618, ev20250922, ev20251108, ev20260629, ev20260722. Regime alto: cota ≥ atenção na referência ou na validade. Treino só com janelas encerradas antes de cada evento; latências do operacional; chuva de latência pelos postos ANA; chuva futura pela previsão arquivada (Open-Meteo previous runs). Gerado por `src/live/backtest_cenarios.py`.

`D0`: rodada meteorológica mais recente (otimista); `D1`: rodada ~24h antes (conservadora). `skill` = 1 − MAE/MAE da persistência. `combinado` é a regra publicada em 04/11; `v2` cai para o GBM puro quando a Ridge não tem entradas.

## Cobertura: % das horas de regime alto com previsão (12h)

| evento     |   combinado D0 |   combinado v2 D0 |   combinado v2 D1 |   operacional |   combinado v2 sem barragens D0 |   combinado v2 ridge+barragens D0 |
|:-----------|---------------:|------------------:|------------------:|--------------:|--------------------------------:|----------------------------------:|
| ev20240430 |             20 |               100 |               100 |            90 |                             100 |                               100 |
| ev20240616 |            100 |               100 |               100 |            83 |                             100 |                               100 |
| ev20241012 |            100 |               100 |               100 |           100 |                             100 |                               100 |
| ev20250618 |            100 |               100 |               100 |            99 |                             100 |                               100 |
| ev20250922 |            100 |               100 |               100 |           100 |                             100 |                               100 |
| ev20251108 |            100 |               100 |               100 |           100 |                             100 |                               100 |
| ev20260629 |            100 |               100 |               100 |           100 |                             100 |                               100 |
| ev20260722 |            100 |               100 |               100 |           100 |                             100 |                               100 |

## Combinado v2 × operacional nos mesmos instantes

| produto         |   h |    n |   mae_cm |   vies_cm |   mae_persistencia_cm |   skill |
|:----------------|----:|-----:|---------:|----------:|----------------------:|--------:|
| combinado v2 D0 |   6 | 2419 |       34 |        -4 |                    94 |    0.64 |
| combinado v2 D0 |  12 | 3283 |       82 |       -10 |                   186 |    0.56 |
| combinado v2 D1 |   6 | 2419 |       34 |        -4 |                    94 |    0.64 |
| combinado v2 D1 |  12 | 3283 |       83 |        -8 |                   186 |    0.55 |
| operacional     |   6 | 2419 |       35 |        -3 |                    94 |    0.63 |
| operacional     |  12 | 3283 |       83 |       -14 |                   186 |    0.56 |

### Regra publicada (v1) × operacional, nos instantes em que a v1 existe

| produto      |   h |    n |   mae_cm |   vies_cm |   mae_persistencia_cm |   skill |
|:-------------|----:|-----:|---------:|----------:|----------------------:|--------:|
| combinado D0 |   6 | 1872 |       33 |        -3 |                   101 |    0.67 |
| combinado D0 |  12 | 2708 |       83 |       -13 |                   196 |    0.58 |
| operacional  |   6 | 1872 |       35 |        -3 |                   101 |    0.66 |
| operacional  |  12 | 2708 |       84 |       -19 |                   196 |    0.57 |

### Por evento (12h, v2 D0 × operacional)

| evento     | produto         |   n |   mae_cm |   vies_cm |   mae_persistencia_cm |   skill |
|:-----------|:----------------|----:|---------:|----------:|----------------------:|--------:|
| ev20240430 | combinado v2 D0 | 709 |      133 |        -2 |                   191 |    0.3  |
| ev20240430 | operacional     | 709 |      119 |       -33 |                   191 |    0.38 |
| ev20240616 | combinado v2 D0 | 588 |       51 |        -2 |                   129 |    0.6  |
| ev20240616 | operacional     | 588 |       56 |        -1 |                   129 |    0.56 |
| ev20241012 | combinado v2 D0 |  93 |       40 |       -35 |                   105 |    0.61 |
| ev20241012 | operacional     |  93 |       37 |       -15 |                   105 |    0.65 |
| ev20250618 | combinado v2 D0 | 788 |       88 |        -7 |                   197 |    0.55 |
| ev20250618 | operacional     | 788 |       77 |        -8 |                   197 |    0.61 |
| ev20250922 | combinado v2 D0 | 179 |       31 |        -2 |                   129 |    0.76 |
| ev20250922 | operacional     | 179 |       53 |        22 |                   129 |    0.59 |
| ev20251108 | combinado v2 D0 | 170 |       63 |         9 |                   158 |    0.6  |
| ev20251108 | operacional     | 170 |       80 |         9 |                   158 |    0.49 |
| ev20260629 | combinado v2 D0 | 189 |       31 |       -21 |                   112 |    0.73 |
| ev20260629 | operacional     | 189 |       38 |         6 |                   112 |    0.66 |
| ev20260722 | combinado v2 D0 | 567 |       86 |       -30 |                   288 |    0.7  |
| ev20260722 | operacional     | 567 |      104 |       -39 |                   288 |    0.64 |

### Por alvo (12h)

| alvo      | produto         |    n |   mae_cm |   vies_cm |   mae_persistencia_cm |   skill |
|:----------|:----------------|-----:|---------:|----------:|----------------------:|--------:|
| Encantado | combinado v2 D0 |  733 |       79 |       -15 |                   222 |    0.64 |
| Encantado | operacional     |  733 |       87 |       -26 |                   222 |    0.61 |
| Estrela   | combinado v2 D0 |  646 |       83 |       -17 |                   209 |    0.6  |
| Estrela   | operacional     |  646 |       75 |       -25 |                   209 |    0.64 |
| Muçum     | combinado v2 D0 | 1904 |       82 |        -5 |                   164 |    0.5  |
| Muçum     | operacional     | 1904 |       83 |        -6 |                   164 |    0.49 |

## Contra o teto (chuva perfeita) e o piso (sem mais chuva)

| produto                |   h |    n |   mae_cm |   vies_cm |   mae_persistencia_cm |   skill |
|:-----------------------|----:|-----:|---------:|----------:|----------------------:|--------:|
| chuva perfeita · gbm   |   6 | 4936 |       36 |        -2 |                   106 |    0.66 |
| chuva perfeita · gbm   |  12 | 5524 |       85 |       -13 |                   198 |    0.57 |
| chuva perfeita · gbm   |  18 | 5828 |      123 |       -29 |                   275 |    0.55 |
| chuva perfeita · gbm   |  24 | 6110 |      138 |       -49 |                   337 |    0.59 |
| chuva perfeita · ridge |   6 | 2468 |       38 |        -1 |                   106 |    0.64 |
| chuva perfeita · ridge |  12 | 2762 |       99 |         6 |                   198 |    0.5  |
| chuva perfeita · ridge |  18 | 2914 |      156 |        15 |                   275 |    0.43 |
| chuva perfeita · ridge |  24 | 3055 |      197 |        21 |                   337 |    0.42 |
| combinado v2 D0        |   6 | 2468 |       33 |        -2 |                   106 |    0.69 |
| combinado v2 D0        |  12 | 2762 |       85 |       -11 |                   198 |    0.57 |
| combinado v2 D0        |  18 | 2914 |      132 |       -24 |                   275 |    0.52 |
| combinado v2 D0        |  24 | 3055 |      164 |       -38 |                   337 |    0.51 |
| sem mais chuva · gbm   |   6 | 2468 |       37 |        -4 |                   106 |    0.66 |
| sem mais chuva · gbm   |  12 | 2762 |       91 |       -32 |                   198 |    0.54 |
| sem mais chuva · gbm   |  18 | 2914 |      144 |       -75 |                   275 |    0.48 |
| sem mais chuva · gbm   |  24 | 3055 |      190 |      -128 |                   337 |    0.44 |
| sem mais chuva · ridge |   6 | 2468 |       38 |       -10 |                   106 |    0.64 |
| sem mais chuva · ridge |  12 | 2762 |       91 |       -48 |                   198 |    0.54 |
| sem mais chuva · ridge |  18 | 2914 |      144 |       -92 |                   275 |    0.48 |
| sem mais chuva · ridge |  24 | 3055 |      194 |      -143 |                   337 |    0.42 |

### Por fase da cheia

| produto                | fase     |     n |   mae_cm |   vies_cm |   mae_persistencia_cm |   skill |
|:-----------------------|:---------|------:|---------:|----------:|----------------------:|--------:|
| chuva perfeita · gbm   | pico     |  1140 |      159 |      -106 |                   354 |    0.55 |
| chuva perfeita · gbm   | recessao | 14712 |       68 |        12 |                   183 |    0.63 |
| chuva perfeita · gbm   | subida   |  6546 |      156 |       -92 |                   333 |    0.53 |
| chuva perfeita · ridge | pico     |   570 |      248 |        26 |                   354 |    0.3  |
| chuva perfeita · ridge | recessao |  7356 |       89 |        16 |                   183 |    0.52 |
| chuva perfeita · ridge | subida   |  3273 |      193 |        -3 |                   333 |    0.42 |
| combinado v2 D0        | pico     |   570 |      142 |       -78 |                   354 |    0.6  |
| combinado v2 D0        | recessao |  7356 |       78 |        17 |                   183 |    0.58 |
| combinado v2 D0        | subida   |  3273 |      168 |       -94 |                   333 |    0.49 |
| sem mais chuva · gbm   | pico     |   570 |      195 |      -169 |                   354 |    0.45 |
| sem mais chuva · gbm   | recessao |  7356 |       73 |        -7 |                   183 |    0.6  |
| sem mais chuva · gbm   | subida   |  3273 |      213 |      -172 |                   333 |    0.36 |
| sem mais chuva · ridge | pico     |   570 |      186 |      -154 |                   354 |    0.47 |
| sem mais chuva · ridge | recessao |  7356 |       79 |       -32 |                   183 |    0.57 |
| sem mais chuva · ridge | subida   |  3273 |      204 |      -164 |                   333 |    0.39 |

## Barragens (defluência da CERAN), h ≥ 12

`sem barragens`: GBM sem defluência. `ridge+barragens`: a Ridge pode usar a defluência, o que cobre as horas sem régua de montante.

| produto                         |   h |    n |   mae_cm |   vies_cm |   mae_persistencia_cm |   skill |
|:--------------------------------|----:|-----:|---------:|----------:|----------------------:|--------:|
| combinado v2 D0                 |  12 | 3489 |       86 |        -6 |                   187 |    0.54 |
| combinado v2 D0                 |  18 | 3662 |      130 |       -14 |                   260 |    0.5  |
| combinado v2 D0                 |  24 | 3851 |      161 |       -30 |                   320 |    0.5  |
| combinado v2 ridge+barragens D0 |  12 | 3489 |       84 |        -5 |                   187 |    0.55 |
| combinado v2 ridge+barragens D0 |  18 | 3662 |      129 |       -13 |                   260 |    0.5  |
| combinado v2 ridge+barragens D0 |  24 | 3851 |      159 |       -26 |                   320 |    0.5  |
| combinado v2 sem barragens D0   |  12 | 3489 |       86 |        -6 |                   187 |    0.54 |
| combinado v2 sem barragens D0   |  18 | 3662 |      131 |       -15 |                   260 |    0.5  |
| combinado v2 sem barragens D0   |  24 | 3851 |      159 |       -30 |                   320 |    0.5  |

### Barragens por evento (12h)

| evento     | produto                         |   n |   mae_cm |   vies_cm |   mae_persistencia_cm |   skill |
|:-----------|:--------------------------------|----:|---------:|----------:|----------------------:|--------:|
| ev20240430 | combinado v2 D0                 | 792 |      147 |        16 |                   195 |    0.25 |
| ev20240430 | combinado v2 ridge+barragens D0 | 792 |      148 |        12 |                   195 |    0.24 |
| ev20240430 | combinado v2 sem barragens D0   | 792 |      147 |        19 |                   195 |    0.25 |
| ev20240616 | combinado v2 D0                 | 705 |       53 |        -5 |                   137 |    0.61 |
| ev20240616 | combinado v2 ridge+barragens D0 | 705 |       56 |        -6 |                   137 |    0.59 |
| ev20240616 | combinado v2 sem barragens D0   | 705 |       56 |        -9 |                   137 |    0.59 |
| ev20241012 | combinado v2 D0                 |  93 |       40 |       -35 |                   105 |    0.61 |
| ev20241012 | combinado v2 ridge+barragens D0 |  93 |       45 |       -42 |                   105 |    0.57 |
| ev20241012 | combinado v2 sem barragens D0   |  93 |       45 |       -39 |                   105 |    0.57 |
| ev20250618 | combinado v2 D0                 | 794 |       88 |        -7 |                   197 |    0.55 |
| ev20250618 | combinado v2 ridge+barragens D0 | 794 |       84 |       -11 |                   197 |    0.57 |
| ev20250618 | combinado v2 sem barragens D0   | 794 |       84 |        -8 |                   197 |    0.57 |
| ev20250922 | combinado v2 D0                 | 179 |       31 |        -2 |                   129 |    0.76 |
| ev20250922 | combinado v2 ridge+barragens D0 | 179 |       31 |         2 |                   129 |    0.76 |
| ev20250922 | combinado v2 sem barragens D0   | 179 |       33 |        -0 |                   129 |    0.74 |
| ev20251108 | combinado v2 D0                 | 170 |       63 |         9 |                   158 |    0.6  |
| ev20251108 | combinado v2 ridge+barragens D0 | 170 |       61 |        15 |                   158 |    0.62 |
| ev20251108 | combinado v2 sem barragens D0   | 170 |       66 |        11 |                   158 |    0.59 |
| ev20260629 | combinado v2 D0                 | 189 |       31 |       -21 |                   112 |    0.73 |
| ev20260629 | combinado v2 ridge+barragens D0 | 189 |       29 |       -15 |                   112 |    0.74 |
| ev20260629 | combinado v2 sem barragens D0   | 189 |       34 |       -22 |                   112 |    0.69 |
| ev20260722 | combinado v2 D0                 | 567 |       86 |       -30 |                   288 |    0.7  |
| ev20260722 | combinado v2 ridge+barragens D0 | 567 |       80 |       -21 |                   288 |    0.72 |
| ev20260722 | combinado v2 sem barragens D0   | 567 |       89 |       -31 |                   288 |    0.69 |

## Membros meteorológicos: MAE (cm) por horizonte

| produto          |   6 |   12 |   18 |   24 |
|:-----------------|----:|-----:|-----:|-----:|
| ECMWF D0 · gbm   |  38 |   86 |  129 |  156 |
| ECMWF D0 · ridge |  37 |   93 |  146 |  184 |
| ECMWF D1 · gbm   |  38 |   89 |  136 |  166 |
| ECMWF D1 · ridge |  39 |   97 |  150 |  194 |
| GEM D0 · gbm     |  38 |   89 |  135 |  163 |
| GEM D0 · ridge   |  40 |  101 |  154 |  193 |
| GEM D1 · gbm     |  38 |   88 |  131 |  157 |
| GEM D1 · ridge   |  40 |  100 |  152 |  191 |
| GFS D0 · gbm     |  38 |   89 |  134 |  164 |
| GFS D0 · ridge   |  41 |  103 |  155 |  197 |
| GFS D1 · gbm     |  38 |   90 |  138 |  170 |
| GFS D1 · ridge   |  42 |  104 |  156 |  201 |
| ICON D0 · gbm    |  38 |   89 |  135 |  164 |
| ICON D0 · ridge  |  39 |   98 |  156 |  195 |
| ICON D1 · gbm    |  38 |   89 |  133 |  163 |
| ICON D1 · ridge  |  40 |  101 |  157 |  200 |
