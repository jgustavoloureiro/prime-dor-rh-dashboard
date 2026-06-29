"""
=============================================================================
PRIME D'OR | RH Analytics Pipeline
Camada Silver — Tratamento, Limpeza e Cálculo de Indicadores
=============================================================================
Aplica regras de qualidade, normalização e calcula os indicadores de RH
derivados dos dados brutos da camada Bronze.

Transformações:
  - Deduplicação e validação de tipos
  - Cálculo de turnover mensal e acumulado
  - Cálculo de absenteísmo (horas perdidas / horas disponíveis)
  - Gap salarial vs P50 e P75 do mercado
  - Custo total por cargo (salário + encargos + benefícios × headcount)
  - Variação OPEX: realizado vs orçado anual
  - Status de alerta por linha orçamentária
  - Posicionamento dos players por indicador

⚠️  DADOS FICTÍCIOS para fins demonstrativos.

Autor: José Gustavo L. C. Silva
       Analista de Dados e Processos | HRBP Analytics
=============================================================================
"""

import json
import os
import datetime
import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------------------------------
BRONZE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "bronze")
SILVER_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "silver")
os.makedirs(SILVER_DIR, exist_ok=True)

TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
HORAS_TRABALHO_MES = 176          # 8h × 22 dias úteis
CUSTO_POR_DESLIGAMENTO = 8500.0   # Custo médio de reposição (R$)
ENCARGOS_FATOR = 1.72             # CLT: 72% de encargos sobre salário bruto


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------
def load_bronze(nome: str) -> pd.DataFrame:
    path = os.path.join(BRONZE_DIR, f"{nome}_raw.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Arquivo bronze não encontrado: {path}\n"
            "Execute primeiro: python 01_bronze_ingestao.py"
        )
    df = pd.read_csv(path, encoding="utf-8-sig")
    print(f"  [load] {nome}: {len(df)} registros")
    return df


def status_alerta(variacao_pct: float) -> str:
    """Classifica desvio orçamentário em semáforo."""
    if abs(variacao_pct) < 5.0:
        return "ok"
    elif abs(variacao_pct) < 10.0:
        return "alerta"
    return "critico"


# ---------------------------------------------------------------------------
# SILVER 1 — Movimentação / Indicadores Mensais
# ---------------------------------------------------------------------------
def transform_movimentacao() -> pd.DataFrame:
    print("[SILVER] Transformando movimentacao...")
    df = load_bronze("movimentacao_hris")

    # Remove colunas de metadados bronze
    df = df[[c for c in df.columns if not c.startswith("_")]]

    # Headcount médio do mês
    df["headcount_fim"] = df["headcount_inicio"] + df["admissoes_raw"] - df["desligamentos_raw"]
    df["headcount_medio"] = ((df["headcount_inicio"] + df["headcount_fim"]) / 2).round(0).astype(int)

    # Turnover mensal % = (adm + desl) / 2 / HC médio × 100
    df["turnover_pct"] = (
        ((df["admissoes_raw"] + df["desligamentos_raw"]) / 2) / df["headcount_medio"] * 100
    ).round(2)

    # Absenteísmo % = afastamentos × 8h / (HC × horas_mês) × 100
    df["absenteismo_pct"] = (
        (df["afastamentos"] * 8) / (df["headcount_medio"] * HORAS_TRABALHO_MES) * 100
    ).round(2)

    # Custo de turnover mensal
    df["custo_turnover_r"] = df["desligamentos_raw"] * CUSTO_POR_DESLIGAMENTO

    # Saldo líquido
    df["saldo_liquido"] = df["admissoes_raw"] - df["desligamentos_raw"]

    # Validações de qualidade
    assert df["turnover_pct"].between(0, 100).all(), "Turnover fora do range 0-100%"
    assert df["absenteismo_pct"].between(0, 50).all(), "Absenteismo fora do range esperado"
    assert (df["headcount_medio"] > 0).all(), "Headcount médio não pode ser zero"

    df["_layer"] = "silver"
    df["_transformed_at"] = TIMESTAMP

    path = os.path.join(SILVER_DIR, "movimentacao_indicadores.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  -> Salvo: {path}")
    return df


# ---------------------------------------------------------------------------
# SILVER 2 — Salários com Gap de Mercado
# ---------------------------------------------------------------------------
def transform_salarios() -> pd.DataFrame:
    print("[SILVER] Transformando pesquisa salarial...")
    df = load_bronze("pesquisa_salarial")

    df = df[[c for c in df.columns if not c.startswith("_")]]

    # Gap absoluto vs P50 e P75
    df["gap_vs_p50"] = df["sal_prime_dor"] - df["p50_mercado"]
    df["gap_vs_p75"] = df["sal_prime_dor"] - df["p75_mercado"]

    # Gap percentual vs P50
    df["gap_pct_vs_p50"] = ((df["sal_prime_dor"] - df["p50_mercado"]) / df["p50_mercado"] * 100).round(1)

    # Posicionamento no mercado
    def posicao_mercado(row):
        if row["sal_prime_dor"] >= row["p75_mercado"]:
            return "acima_p75"
        elif row["sal_prime_dor"] >= row["p50_mercado"]:
            return "entre_p50_p75"
        elif row["sal_prime_dor"] >= row["p25_mercado"]:
            return "entre_p25_p50"
        return "abaixo_p25"

    df["posicao_mercado"] = df.apply(posicao_mercado, axis=1)

    # Custo total mensal por cargo = (sal × encargos_fator + benefícios) × headcount
    df["custo_mensal_total"] = (
        (df["sal_prime_dor"] * ENCARGOS_FATOR + df["beneficios_mensais"]) * df["headcount_unidade"]
    ).round(0).astype(int)

    df["custo_anual_total"] = df["custo_mensal_total"] * 12

    # Custo de turnover hipotético se perder 1 colaborador do cargo
    df["custo_reposicao_unit"] = CUSTO_POR_DESLIGAMENTO

    # Risco de rotatividade (flag se gap_pct_vs_p50 < -10%)
    df["flag_risco_retencao"] = df["gap_pct_vs_p50"] < -10.0

    # Validações
    assert (df["custo_mensal_total"] > 0).all(), "Custo mensal não pode ser zero"
    assert df["posicao_mercado"].notna().all(), "Posicionamento não pode ser nulo"

    df["_layer"] = "silver"
    df["_transformed_at"] = TIMESTAMP

    path = os.path.join(SILVER_DIR, "salarios_tratados.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  -> Salvo: {path}")
    return df


# ---------------------------------------------------------------------------
# SILVER 3 — Benchmarks Normalizados
# ---------------------------------------------------------------------------
def transform_benchmarks() -> pd.DataFrame:
    print("[SILVER] Transformando benchmarks de players...")
    df = load_bronze("benchmarks_players")

    df = df[[c for c in df.columns if not c.startswith("_")]]

    # Preenche nulos com mediana (apenas para numeric)
    num_cols = ["colaboradores", "receita_bi"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Ranking por indicador (menor turnover = melhor)
    df["rank_turnover"]     = df["turnover_pct"].rank(ascending=True).astype(int)
    df["rank_absenteismo"]  = df["absenteismo_pct"].rank(ascending=True).astype(int)
    df["rank_enps"]         = df["enps_estimado"].rank(ascending=False).astype(int)
    df["rank_td"]           = df["td_horas_ano"].rank(ascending=False).astype(int)

    # Score composto de RH (média dos rankings — menor = melhor)
    df["score_rh_composto"] = (
        df["rank_turnover"] + df["rank_absenteismo"] + df["rank_enps"] + df["rank_td"]
    ) / 4

    df["_layer"] = "silver"
    df["_transformed_at"] = TIMESTAMP

    path = os.path.join(SILVER_DIR, "benchmarks_normalizados.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  -> Salvo: {path}")
    return df


# ---------------------------------------------------------------------------
# SILVER 4 — OPEX com Variação e Status
# ---------------------------------------------------------------------------
def transform_orcamento() -> tuple:
    print("[SILVER] Transformando orcamento OPEX/CAPEX...")

    # OPEX
    df_opex = load_bronze("opex")
    df_opex = df_opex[[c for c in df_opex.columns if not c.startswith("_")]]

    df_opex["orcado_anual"]   = df_opex["orcado_mensal"] * 12
    df_opex["variacao_r"]     = df_opex["realizado_anual"] - df_opex["orcado_anual"]
    df_opex["variacao_pct"]   = (df_opex["variacao_r"] / df_opex["orcado_anual"] * 100).round(1)
    df_opex["status_alerta"]  = df_opex["variacao_pct"].apply(status_alerta)
    df_opex["pct_orcado_exec"]= (df_opex["realizado_anual"] / df_opex["orcado_anual"] * 100).round(1)

    # CAPEX
    df_capex = load_bronze("capex")
    df_capex = df_capex[[c for c in df_capex.columns if not c.startswith("_")]]

    df_capex["pct_execucao"]  = (df_capex["executado"] / df_capex["valor_planejado"] * 100).round(1)
    df_capex["saldo"]         = df_capex["valor_planejado"] - df_capex["executado"]
    df_capex["status_capex"]  = df_capex["pct_execucao"].apply(
        lambda p: "concluido" if p >= 100 else ("em_execucao" if p > 0 else "planejado")
    )

    for df, nome in [(df_opex, "opex_tratado"), (df_capex, "capex_tratado")]:
        df["_layer"] = "silver"
        df["_transformed_at"] = TIMESTAMP
        path = os.path.join(SILVER_DIR, f"{nome}.csv")
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"  -> Salvo: {path}")

    return df_opex, df_capex


# ---------------------------------------------------------------------------
# SILVER 5 — KPIs Consolidados da Unidade
# ---------------------------------------------------------------------------
def calc_kpis_unidade(df_mov: pd.DataFrame, df_sal: pd.DataFrame) -> dict:
    print("[SILVER] Calculando KPIs consolidados da unidade...")

    kpis = {
        # Headcount
        "headcount_atual":           int(df_mov["headcount_fim"].iloc[-1]),
        "headcount_medio_ano":       int(df_mov["headcount_medio"].mean().round(0)),

        # Turnover
        "turnover_anual_pct":        round(df_mov["turnover_pct"].sum(), 1),
        "turnover_medio_mensal_pct": round(df_mov["turnover_pct"].mean(), 2),
        "desligamentos_total":       int(df_mov["desligamentos_raw"].sum()),
        "admissoes_total":           int(df_mov["admissoes_raw"].sum()),

        # Absenteísmo
        "absenteismo_medio_pct":     round(df_mov["absenteismo_pct"].mean(), 1),
        "absenteismo_pico_mes":      df_mov.loc[df_mov["absenteismo_pct"].idxmax(), "mes"],
        "afastamentos_total":        int(df_mov["afastamentos"].sum()),

        # Custos
        "custo_turnover_anual_r":    int(df_mov["custo_turnover_r"].sum()),
        "custo_folha_mensal_est":    int(df_sal["custo_mensal_total"].sum()),
        "custo_folha_anual_est":     int(df_sal["custo_anual_total"].sum()),

        # Salários e mercado
        "cargos_abaixo_p50":         int(df_sal[df_sal["gap_vs_p50"] < 0].shape[0]),
        "cargos_acima_p75":          int(df_sal[df_sal["gap_vs_p75"] > 0].shape[0]),
        "cargos_flag_retencao":      int(df_sal["flag_risco_retencao"].sum()),

        # Metadados
        "data_referencia":           "Jun/2025",
        "unidade":                   "Hospital RJ",
        "_calculated_at":            TIMESTAMP,
        "_layer":                    "silver",
    }

    path = os.path.join(SILVER_DIR, "kpis_unidade.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(kpis, f, ensure_ascii=False, indent=2)
    print(f"  -> Salvo: {path}")
    return kpis


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def run():
    print("=" * 60)
    print("PRIME D'OR | Pipeline de Dados RH")
    print("Camada SILVER — Tratamento e Indicadores")
    print(f"Timestamp: {TIMESTAMP}")
    print("=" * 60)

    df_mov             = transform_movimentacao()
    df_sal             = transform_salarios()
    df_bench           = transform_benchmarks()
    df_opex, df_capex  = transform_orcamento()
    kpis               = calc_kpis_unidade(df_mov, df_sal)

    print("\n[SILVER] Resumo dos KPIs calculados:")
    print(f"  Headcount atual:       {kpis['headcount_atual']}")
    print(f"  Turnover anual:        {kpis['turnover_anual_pct']}%")
    print(f"  Absenteismo medio:     {kpis['absenteismo_medio_pct']}%")
    print(f"  Custo turnover/ano:    R$ {kpis['custo_turnover_anual_r']:,.0f}")
    print(f"  Cargos abaixo P50:     {kpis['cargos_abaixo_p50']}")
    print(f"  Cargos risco retencao: {kpis['cargos_flag_retencao']}")

    print("=" * 60)
    print("[SILVER] Transformacoes concluidas.")
    print("Proxima etapa: executar 03_gold_modelagem.py")
    print("=" * 60)


if __name__ == "__main__":
    run()
