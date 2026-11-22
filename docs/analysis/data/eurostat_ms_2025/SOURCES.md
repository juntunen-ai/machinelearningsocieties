# Eurostat member-state inputs for the coherence appendix

Retrieved 2026-11-22 from the Eurostat dissemination API (JSON-stat), 27 member states, reference year 2025:

- `eb.json`: `isoc_eb_ai`, indic_is = E_AI_TANY, E_AI_TGE3, E_AI_TAR, E_AI_TPVSG; unit = PC_ENT; size_emp = GE10; nace_r2 = C10-S951_X_K.
- `iaiu.json`: `isoc_ai_iaiu`, indic_is = I_IUAI; unit = PC_IND; ind_type = IND_TOTAL.
- `an6.json`: `nama_10_an6`, unit = PC_GDP; asset10 = N1132G, N117G; years 2024 and 2025 (dataset updated 2026-11-05).

Same series, filters and goalposts as D1–D4 and K1 in `index/method.v1.0.json`. Used only by `scripts/analysis/coherence_eu27.py`; never by the compiler.
