# Fase 11 — Placar, produto combinado e benchmarks da região

Data: 04/11/2026. Código: `src/live/placar.py`, `src/live/combinado.py`,
`src/live/atualizar.py`. Placar completo em `reports/16_placar.md`.

Não é sistema de alerta (ver `LIMITACOES.md`).

## 1. O que o placar mostrou

4.399 pares previsto × observado de 33 emissões reais das cheias de 21/09 e
28–30/09/2026, conferidos com a cota da ANA até 04/11. Persistência = repetir a
cota da referência.

| h | operacional MAE (cm) | viés | skill | combinado MAE (cm) | viés | skill |
|---|---|---|---|---|---|---|
| 3 | 23 | −10 | 0,76 | 23 | −11 | 0,75 |
| 6 | 73 | −29 | 0,64 | 54 | −17 | 0,73 |
| 9 | 105 | −48 | 0,62 | — | — | — |
| 12 | 131 | −71 | 0,60 | 85 | +5 | 0,74 |
| 18 | — | — | — | 95 | +49 | 0,76 |
| 24 | — | — | — | 87 | +42 | 0,81 |

As amostras dos dois produtos não são idênticas. Na comparação pareada (mesma
execução, alvo e validade), o combinado reduziu o MAE em todos os casos:
Encantado 12h 144 → 83 cm, Muçum 6–12h 162 → 140, Estrela 12h 166 → 114.
Até 6h ele é o próprio linear operacional, por construção.

Diagnóstico:

- **O operacional subestima sistematicamente as subidas** (viés −50 a −140 cm
  em 9–12h) porque não enxerga a chuva que ainda vai cair. É a mesma
  limitação do SACE (seção 3).
- **Os cenários com chuva prevista quase zeram esse viés** em 6–12h.
- Por fase: a Ridge acerta o pico (MAE ~69 cm contra ~165 do GBM) e o GBM a
  recessão (~74 contra ~110). A média dos dois é melhor que cada um nas três
  fases, sem precisar detectar a fase em tempo real.
- **Novo problema:** na recessão o combinado superestima (+52 cm), porque os
  cenários descem devagar demais. É o próximo alvo.

## 2. Regra do produto combinado

- h ≤ 6 com motor operacional linear: linear operacional.
- demais: média de Ridge e GBM dos cenários, cada um como mediana de ECMWF,
  GFS, ICON e GEM. Envelope = mínimo e máximo dos membros com chuva; "sem
  mais chuva" como referência inferior.

**Ressalva:** a regra foi escolhida olhando os pares de setembro (seleção
dentro da amostra). Testei cinco variantes; a escolhida é a mais simples entre
as melhores, e não a de menor erro em cada horizonte. Só um backtest fora da
amostra confirma o ganho (seção 4).

## 3. Benchmarks e estudos da região

| Referência | Método | Antecedência | Erro publicado |
|---|---|---|---|
| SACE/SGB (manual 2014, boletins 2025) | regressão cota-cota em diferenças, sem chuva | Muçum/Encantado 4h, Estrela 6h | Encantado 4h, nov/2023: MAE 47 cm, NSE 0,98 (Oliveira et al., SBRH 2025) |
| Mendes, Marcuzzo & Buffon (SBRH 2025) | AR linear treinado a partir da cota de atenção | 2–4h | 4h: MAE ~72 cm Muçum, ~54 Encantado, ~31 Estrela (sem validação independente) |
| Finck (IPH-UFRGS, 2020) | redes neurais + chuva com filtro gama | 4–24h | MAE 12–20 cm em 2017, quase todo vazante: não comparável |
| IPH-UFRGS (MGB-IPH + Eta/BRAMS) | chuva-vazão com chuva prevista | dias | sem métricas publicadas |
| Google Flood Hub (Estrela) | LSTM global diária | 1–5 dias | sem previsão em 04/11/2026; sem avaliação no Taquari |

O que isso significa:

- Nosso linear de 3h (MAE ~23 cm nas cheias de setembro) está no nível do
  SACE de 4h ou melhor. Os dados não são do mesmo evento; a comparação é
  indicativa.
- O próprio estudo do SACE registra subestimação na ascensão. É estrutural em
  modelos cota-cota: acima de ~6h só chuva prevista ou chuva-vazão resolvem
  (Collischonn et al., II END 2020: Lajeado precisa de ~25h).
- O "ganho de 86%" do estudo de 2025 é a fração de métricas que melhoraram,
  não redução de erro, e sem validação independente. Coerente com a
  Armadilha 2 não ter replicado aqui.
- ECMWF e GFS subestimaram a chuva de maio/2024 em até 60 mm com 24h
  (Oliveira et al., EGU26-20249). O viés da chuva prevista precisa ser medido.
- A defluência da CERAN deu quase 24h de antecedência para Lajeado em
  set/2023 (nota IPH): é a melhor variável que temos para 12–24h.

Fontes completas: SGB/CPRM 2014 (rigeo doc/24596), Oliveira, Fan, Bravo,
Marcuzzo & Buffon 2025 (rigeo doc/25766), Mendes, Marcuzzo & Buffon 2025
(rigeo doc/25758), Finck 2020 (lume 10183/213406), Collischonn et al. 2020
(II END 0136), Siqueira et al. RBRH 21 2016, Frame et al. HESS 26:3377 2022,
Li et al. HESS 20:3561 2016 (ERRIS), Weerts et al. HESS 15:255 2011,
Nearing et al. Nature 627 2024.

## 4. Próximos passos, em ordem

1. **Backtest fora da amostra com previsão de chuva arquivada.** A previous
   runs API do Open-Meteo devolve, para 2024 em diante, a previsão emitida
   ~24h antes nos quatro modelos (verificado para 29/04–01/05/2024). Isso
   permite rodar os cenários nas cheias de 2024–2025 como se fossem ao vivo,
   confirmar ou derrubar a regra combinada e medir o viés da chuva prevista.
2. **Recessão:** corrigir a superestimação dos cenários. Candidatos: AR(1) no
   erro recente (ERRIS), mais forte em 3–6h, e um membro de recessão
   exponencial.
3. **Componente físico para picos fora do treino:** propagação da defluência
   da CERAN (lag-and-route/Muskingum) como entrada, com o ML prevendo o
   resíduo.
4. **9h nos cenários** (hoje só 6/12/18/24) e faixas por regressão quantílica.
5. **Automação** do ciclo atualizar → emitir → cenários → combinado → placar.
