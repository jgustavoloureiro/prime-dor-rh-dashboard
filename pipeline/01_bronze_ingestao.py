"""
=============================================================================
PRIME D'OR | RH Analytics Pipeline
Camada Bronze — Ingestão de Dados Brutos
=============================================================================
Responsável pela ingestão e armazenamento raw das fontes de dados públicas
e internas. Nenhuma transformação é aplicada nesta camada.

Fontes:
  - Relatório de Sustentabilidade / ESG D'Or 2023
  - ANAHP Observatório 2023/2024
  - Robert Half Guia Salarial 2024
  - Michael Robert MR Survey 2024
  - Glassdoor / Indeed (percepção pública)
  - HRIS interno (simulado para fins demonstrativos)

⚠️  DADOS FICTÍCIOS para fins demonstrativos.
    Em produção, conectar às APIs e sistemas reais (HRIS, ServiceNow, etc.)

Autor: José Gustavo L. C. Silva
       Analista de Dados e Processos | HRBP Analytics
=============================================================================
"""

import json
import os
import datetime
import pandas as pd

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO
# ---------------------------------------------------------------------------
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "bronze")
os.makedirs(RAW_DIR, exist_ok=True)

TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
META = {
    "pipeline_version": "1.0.0",
    "layer": "bronze",
    "ingested_at": TIMESTAMP,
    "author": "José Gustavo L. C. Silva",
    "note": "Dados fictícios para fins demonstrativos"
}


# ---------------------------------------------------------------------------
# FONTE 1 — HRIS / Movimentação de Pessoal (simulado)
# ---------------------------------------------------------------------------
def ingest_movimentacao_hris():
    """
    Simula extração do HRIS de movimentações mensais de pessoal.
    Em produção: conectar via API REST do SuccessFactors / SAP HCM / TOTVS RH.
    """
    print("[BRONZE] Ingerindo movimentações HRIS...")

    raw_movimentacao = [
        {"mes": "Jan", "mes_num": 1, "admissoes_raw": 9,  "desligamentos_raw": 7,  "headcount_inicio": 510, "horas_extras_h": 1820, "afastamentos": 12},
        {"mes": "Fev", "mes_num": 2, "admissoes_raw": 7,  "desligamentos_raw": 6,  "headcount_inicio": 512, "horas_extras_h": 1640, "afastamentos": 10},
        {"mes": "Mar", "mes_num": 3, "admissoes_raw": 6,  "desligamentos_raw": 10, "headcount_inicio": 513, "horas_extras_h": 2100, "afastamentos": 14},
        {"mes": "Abr", "mes_num": 4, "admissoes_raw": 8,  "desligamentos_raw": 7,  "headcount_inicio": 509, "horas_extras_h": 1750, "afastamentos": 11},
        {"mes": "Mai", "mes_num": 5, "admissoes_raw": 8,  "desligamentos_raw": 7,  "headcount_inicio": 510, "horas_extras_h": 1800, "afastamentos": 13},
        {"mes": "Jun", "mes_num": 6, "admissoes_raw": 7,  "desligamentos_raw": 8,  "headcount_inicio": 511, "horas_extras_h": 2050, "afastamentos": 18},
        {"mes": "Jul", "mes_num": 7, "admissoes_raw": 5,  "desligamentos_raw": 11, "headcount_inicio": 510, "horas_extras_h": 2380, "afastamentos": 22},
        {"mes": "Ago", "mes_num": 8, "admissoes_raw": 8,  "desligamentos_raw": 7,  "headcount_inicio": 504, "horas_extras_h": 1690, "afastamentos": 15},
        {"mes": "Set", "mes_num": 9, "admissoes_raw": 9,  "desligamentos_raw": 6,  "headcount_inicio": 505, "horas_extras_h": 1710, "afastamentos": 13},
        {"mes": "Out", "mes_num": 10,"admissoes_raw": 6,  "desligamentos_raw": 10, "headcount_inicio": 508, "horas_extras_h": 1880, "afastamentos": 16},
        {"mes": "Nov", "mes_num": 11,"admissoes_raw": 8,  "desligamentos_raw": 7,  "headcount_inicio": 504, "horas_extras_h": 1740, "afastamentos": 14},
        {"mes": "Dez", "mes_num": 12,"admissoes_raw": 9,  "desligamentos_raw": 6,  "headcount_inicio": 505, "horas_extras_h": 1960, "afastamentos": 20},
    ]

    df = pd.DataFrame(raw_movimentacao)
    df["_ingested_at"] = TIMESTAMP
    df["_source"] = "HRIS_simulado"
    df["_layer"] = "bronze"

    path = os.path.join(RAW_DIR, "movimentacao_hris_raw.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  -> Salvo: {path} ({len(df)} registros)")
    return df


# ---------------------------------------------------------------------------
# FONTE 2 — Pesquisa Salarial (Robert Half + MR Survey)
# ---------------------------------------------------------------------------
def ingest_pesquisa_salarial():
    """
    Dados brutos de pesquisa salarial por cargo e empresa.
    Fonte: Robert Half Guia Salarial 2024 + MR Survey 2024.
    """
    print("[BRONZE] Ingerindo pesquisa salarial de mercado...")

    raw_salarios = [
        {"cargo": "HRBP Senior",          "nivel": "Senior",      "area": "Gente & Gestao", "headcount_unidade": 4,
         "sal_prime_dor": 12800, "sal_sirio": 15200, "sal_hapvida": 9800,  "sal_fleury": 13500, "sal_dasa": 11200,
         "p25_mercado": 10500, "p50_mercado": 12500, "p75_mercado": 14800, "p90_mercado": 17000,
         "bonus_anual_pct": 15, "beneficios_mensais": 2200, "encargos_pct": 72.0},
        {"cargo": "HRBP Pleno",            "nivel": "Pleno",       "area": "Gente & Gestao", "headcount_unidade": 8,
         "sal_prime_dor": 8900, "sal_sirio": 10500, "sal_hapvida": 7200,  "sal_fleury": 9400,  "sal_dasa": 8100,
         "p25_mercado": 7200, "p50_mercado": 8800, "p75_mercado": 10200, "p90_mercado": 12000,
         "bonus_anual_pct": 10, "beneficios_mensais": 1800, "encargos_pct": 72.0},
        {"cargo": "Analista RH Senior",    "nivel": "Senior",      "area": "Gente & Gestao", "headcount_unidade": 6,
         "sal_prime_dor": 7200, "sal_sirio": 8800,  "sal_hapvida": 5900,  "sal_fleury": 7800,  "sal_dasa": 6900,
         "p25_mercado": 5800, "p50_mercado": 7000, "p75_mercado": 8500, "p90_mercado": 10000,
         "bonus_anual_pct": 8, "beneficios_mensais": 1600, "encargos_pct": 72.0},
        {"cargo": "Analista RH Pleno",     "nivel": "Pleno",       "area": "Gente & Gestao", "headcount_unidade": 10,
         "sal_prime_dor": 5400, "sal_sirio": 6500,  "sal_hapvida": 4400,  "sal_fleury": 5800,  "sal_dasa": 5100,
         "p25_mercado": 4200, "p50_mercado": 5300, "p75_mercado": 6400, "p90_mercado": 7500,
         "bonus_anual_pct": 6, "beneficios_mensais": 1400, "encargos_pct": 72.0},
        {"cargo": "Analista RH Junior",    "nivel": "Junior",      "area": "Gente & Gestao", "headcount_unidade": 8,
         "sal_prime_dor": 3200, "sal_sirio": 3900,  "sal_hapvida": 2800,  "sal_fleury": 3500,  "sal_dasa": 3100,
         "p25_mercado": 2600, "p50_mercado": 3100, "p75_mercado": 3800, "p90_mercado": 4500,
         "bonus_anual_pct": 0, "beneficios_mensais": 1200, "encargos_pct": 72.0},
        {"cargo": "Enfermeiro Senior",     "nivel": "Senior",      "area": "Assistencial",   "headcount_unidade": 52,
         "sal_prime_dor": 8400, "sal_sirio": 11200, "sal_hapvida": 6500,  "sal_fleury": 7200,  "sal_dasa": 7800,
         "p25_mercado": 6200, "p50_mercado": 8000, "p75_mercado": 10000, "p90_mercado": 12500,
         "bonus_anual_pct": 5, "beneficios_mensais": 1800, "encargos_pct": 72.0},
        {"cargo": "Enfermeiro Pleno",      "nivel": "Pleno",       "area": "Assistencial",   "headcount_unidade": 68,
         "sal_prime_dor": 6200, "sal_sirio": 8000,  "sal_hapvida": 4900,  "sal_fleury": 5800,  "sal_dasa": 5900,
         "p25_mercado": 4800, "p50_mercado": 5900, "p75_mercado": 7500, "p90_mercado": 9000,
         "bonus_anual_pct": 0, "beneficios_mensais": 1600, "encargos_pct": 72.0},
        {"cargo": "Tecnico Enfermagem",    "nivel": "Tecnico",     "area": "Assistencial",   "headcount_unidade": 184,
         "sal_prime_dor": 3800, "sal_sirio": 4900,  "sal_hapvida": 3100,  "sal_fleury": 3600,  "sal_dasa": 3700,
         "p25_mercado": 3000, "p50_mercado": 3700, "p75_mercado": 4500, "p90_mercado": 5500,
         "bonus_anual_pct": 0, "beneficios_mensais": 1200, "encargos_pct": 72.0},
        {"cargo": "Auxiliar Enfermagem",   "nivel": "Operacional", "area": "Assistencial",   "headcount_unidade": 96,
         "sal_prime_dor": 2600, "sal_sirio": 3200,  "sal_hapvida": 2200,  "sal_fleury": 2700,  "sal_dasa": 2500,
         "p25_mercado": 2000, "p50_mercado": 2500, "p75_mercado": 3100, "p90_mercado": 3800,
         "bonus_anual_pct": 0, "beneficios_mensais": 1000, "encargos_pct": 72.0},
        {"cargo": "Medico Plantonista",    "nivel": "Especialista","area": "Assistencial",   "headcount_unidade": 38,
         "sal_prime_dor": 18500,"sal_sirio": 24000, "sal_hapvida": 14000, "sal_fleury": 16000, "sal_dasa": 17500,
         "p25_mercado": 14000,"p50_mercado": 18000,"p75_mercado": 23000,"p90_mercado": 28000,
         "bonus_anual_pct": 10, "beneficios_mensais": 2800, "encargos_pct": 72.0},
        {"cargo": "Coordenador Medico",    "nivel": "Gestao",      "area": "Assistencial",   "headcount_unidade": 6,
         "sal_prime_dor": 22000,"sal_sirio": 28000, "sal_hapvida": 17000, "sal_fleury": 20000, "sal_dasa": 21000,
         "p25_mercado": 17000,"p50_mercado": 21000,"p75_mercado": 27000,"p90_mercado": 33000,
         "bonus_anual_pct": 15, "beneficios_mensais": 3200, "encargos_pct": 72.0},
        {"cargo": "Gerente Unidade",       "nivel": "Gestao",      "area": "Gestao",         "headcount_unidade": 3,
         "sal_prime_dor": 16500,"sal_sirio": 22000, "sal_hapvida": 12000, "sal_fleury": 15000, "sal_dasa": 15500,
         "p25_mercado": 13000,"p50_mercado": 16000,"p75_mercado": 21000,"p90_mercado": 26000,
         "bonus_anual_pct": 20, "beneficios_mensais": 3000, "encargos_pct": 72.0},
        {"cargo": "Supervisor Operacional","nivel": "Lideranca",   "area": "Gestao",         "headcount_unidade": 12,
         "sal_prime_dor": 7800, "sal_sirio": 9500,  "sal_hapvida": 5900,  "sal_fleury": 7200,  "sal_dasa": 7300,
         "p25_mercado": 6000, "p50_mercado": 7500, "p75_mercado": 9000, "p90_mercado": 11000,
         "bonus_anual_pct": 8, "beneficios_mensais": 1700, "encargos_pct": 72.0},
        {"cargo": "Assist. Administrativo","nivel": "Operacional", "area": "Administrativo", "headcount_unidade": 28,
         "sal_prime_dor": 2400, "sal_sirio": 2900,  "sal_hapvida": 2000,  "sal_fleury": 2500,  "sal_dasa": 2300,
         "p25_mercado": 1900, "p50_mercado": 2300, "p75_mercado": 2800, "p90_mercado": 3400,
         "bonus_anual_pct": 0, "beneficios_mensais": 900, "encargos_pct": 72.0},
        {"cargo": "Analista Financeiro",   "nivel": "Pleno",       "area": "Administrativo", "headcount_unidade": 6,
         "sal_prime_dor": 6800, "sal_sirio": 8200,  "sal_hapvida": 5400,  "sal_fleury": 7000,  "sal_dasa": 6500,
         "p25_mercado": 5400, "p50_mercado": 6600, "p75_mercado": 8000, "p90_mercado": 9500,
         "bonus_anual_pct": 8, "beneficios_mensais": 1500, "encargos_pct": 72.0},
        {"cargo": "Nutricionista",         "nivel": "Especialista","area": "Assistencial",   "headcount_unidade": 8,
         "sal_prime_dor": 4800, "sal_sirio": 6200,  "sal_hapvida": 3800,  "sal_fleury": 4500,  "sal_dasa": 4600,
         "p25_mercado": 3800, "p50_mercado": 4700, "p75_mercado": 5900, "p90_mercado": 7000,
         "bonus_anual_pct": 0, "beneficios_mensais": 1300, "encargos_pct": 72.0},
        {"cargo": "Assistente Social",     "nivel": "Especialista","area": "Assistencial",   "headcount_unidade": 5,
         "sal_prime_dor": 4200, "sal_sirio": 5500,  "sal_hapvida": 3400,  "sal_fleury": 4000,  "sal_dasa": 4100,
         "p25_mercado": 3300, "p50_mercado": 4100, "p75_mercado": 5200, "p90_mercado": 6200,
         "bonus_anual_pct": 0, "beneficios_mensais": 1200, "encargos_pct": 72.0},
        {"cargo": "Farmaceutico",          "nivel": "Especialista","area": "Assistencial",   "headcount_unidade": 7,
         "sal_prime_dor": 6400, "sal_sirio": 8000,  "sal_hapvida": 5100,  "sal_fleury": 6000,  "sal_dasa": 6200,
         "p25_mercado": 5000, "p50_mercado": 6200, "p75_mercado": 7700, "p90_mercado": 9200,
         "bonus_anual_pct": 5, "beneficios_mensais": 1500, "encargos_pct": 72.0},
    ]

    df = pd.DataFrame(raw_salarios)
    df["_ingested_at"] = TIMESTAMP
    df["_source"] = "Robert_Half_MR_Survey_2024"
    df["_layer"] = "bronze"

    path = os.path.join(RAW_DIR, "pesquisa_salarial_raw.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  -> Salvo: {path} ({len(df)} cargos)")
    return df


# ---------------------------------------------------------------------------
# FONTE 3 — Benchmarks de Players (ANAHP + ESG público)
# ---------------------------------------------------------------------------
def ingest_benchmarks_players():
    """
    Indicadores de RH dos principais players do setor hospitalar privado.
    Fonte: ANAHP Observatório 2024, Relatórios ESG públicos, Glassdoor.
    """
    print("[BRONZE] Ingerindo benchmarks de players de mercado...")

    raw_players = [
        {"empresa": "Prime D'Or",    "segmento": "Hospitalar Premium",    "colaboradores": 60000, "turnover_pct": 18.0, "absenteismo_pct": 4.8, "enps_estimado": 42, "mulheres_pct": 75, "td_horas_ano": 32, "custo_turnover_k": 8.5,  "receita_bi": 51.3, "fonte": "ESG_2023"},
        {"empresa": "Sirio-Libanes", "segmento": "Hospitalar Premium",    "colaboradores": 9000,  "turnover_pct": 12.0, "absenteismo_pct": 4.2, "enps_estimado": 51, "mulheres_pct": 73, "td_horas_ano": 40, "custo_turnover_k": 12.0, "receita_bi": 2.8,  "fonte": "Relatorio_Anual_2023"},
        {"empresa": "Hapvida_NDI",   "segmento": "Planos + Hospitais",    "colaboradores": 80000, "turnover_pct": 26.0, "absenteismo_pct": 5.8, "enps_estimado": 18, "mulheres_pct": 70, "td_horas_ano": 18, "custo_turnover_k": 6.5,  "receita_bi": 28.0, "fonte": "RI_2023"},
        {"empresa": "Fleury_Pardini","segmento": "Diagnosticos",          "colaboradores": 22000, "turnover_pct": 20.0, "absenteismo_pct": 4.5, "enps_estimado": 38, "mulheres_pct": 72, "td_horas_ano": 28, "custo_turnover_k": 9.0,  "receita_bi": 5.8,  "fonte": "ESG_2023"},
        {"empresa": "Dasa_Amil",     "segmento": "Diagnosticos + Hosp.",  "colaboradores": 35000, "turnover_pct": 24.0, "absenteismo_pct": 5.5, "enps_estimado": 22, "mulheres_pct": 69, "td_horas_ano": 20, "custo_turnover_k": 7.5,  "receita_bi": 9.9,  "fonte": "RI_2024"},
        {"empresa": "Mater_Dei",     "segmento": "Hospitalar Regional",   "colaboradores": 8000,  "turnover_pct": 21.0, "absenteismo_pct": 5.0, "enps_estimado": 28, "mulheres_pct": 68, "td_horas_ano": 24, "custo_turnover_k": 8.0,  "receita_bi": 2.1,  "fonte": "Glassdoor_2024"},
        {"empresa": "ANAHP_Media",   "segmento": "Benchmark Setor",       "colaboradores": None,  "turnover_pct": 22.0, "absenteismo_pct": 5.3, "enps_estimado": 30, "mulheres_pct": 68, "td_horas_ano": 24, "custo_turnover_k": 8.0,  "receita_bi": None, "fonte": "ANAHP_Observatorio_2024"},
    ]

    df = pd.DataFrame(raw_players)
    df["_ingested_at"] = TIMESTAMP
    df["_source"] = "ANAHP_ESG_Glassdoor"
    df["_layer"] = "bronze"

    path = os.path.join(RAW_DIR, "benchmarks_players_raw.csv")
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"  -> Salvo: {path} ({len(df)} players)")
    return df


# ---------------------------------------------------------------------------
# FONTE 4 — Orçamento OPEX/CAPEX (simulado do sistema financeiro)
# ---------------------------------------------------------------------------
def ingest_orcamento():
    """
    Dados brutos do orçamento de RH — OPEX e CAPEX.
    Em produção: extrair do SAP FI/CO ou sistema de gestão orçamentária.
    """
    print("[BRONZE] Ingerindo orçamento OPEX/CAPEX...")

    raw_opex = [
        {"linha": "Salarios e Encargos",        "categoria": "Folha",       "orcado_mensal": 3650000, "realizado_anual": 45358276},
        {"linha": "Beneficios VT+VR+Plano",     "categoria": "Beneficios",  "orcado_mensal": 820000,  "realizado_anual": 9849844},
        {"linha": "Horas Extras",               "categoria": "Folha",       "orcado_mensal": 145000,  "realizado_anual": 1863542},
        {"linha": "Recrutamento e Selecao",     "categoria": "R&S",         "orcado_mensal": 92000,   "realizado_anual": 1146977},
        {"linha": "Treinamento e Desenvolvimento","categoria": "T&D",       "orcado_mensal": 68000,   "realizado_anual": 872678},
        {"linha": "Medicina do Trabalho",       "categoria": "SSO",         "orcado_mensal": 38000,   "realizado_anual": 468343},
        {"linha": "Uniformes e EPIs",           "categoria": "Operacional", "orcado_mensal": 24000,   "realizado_anual": 296838},
        {"linha": "Software RH HRIS",           "categoria": "TI",          "orcado_mensal": 18000,   "realizado_anual": 212431},
        {"linha": "Consultorias RH",            "categoria": "Outros",      "orcado_mensal": 15000,   "realizado_anual": 174038},
        {"linha": "Eventos Corporativos",       "categoria": "Engajamento", "orcado_mensal": 22000,   "realizado_anual": 285435},
    ]

    raw_capex = [
        {"projeto": "Sistema HRIS Upgrade",           "categoria": "TI",             "valor_planejado": 480000, "executado": 320000, "previsao": "Dez/2025"},
        {"projeto": "Sala de Treinamento Reforma",    "categoria": "Infraestrutura", "valor_planejado": 220000, "executado": 180000, "previsao": "Set/2025"},
        {"projeto": "Plataforma LMS e-Learning",      "categoria": "TI",             "valor_planejado": 160000, "executado": 160000, "previsao": "Jun/2025"},
        {"projeto": "Equipamentos Medicina Trabalho", "categoria": "Equipamentos",   "valor_planejado": 95000,  "executado": 42000,  "previsao": "Nov/2025"},
        {"projeto": "Mobiliario RH Nova Sede",        "categoria": "Infraestrutura", "valor_planejado": 85000,  "executado": 0,      "previsao": "Jan/2026"},
        {"projeto": "Software Recrutamento ATS",      "categoria": "TI",             "valor_planejado": 72000,  "executado": 72000,  "previsao": "Mar/2025"},
    ]

    df_opex  = pd.DataFrame(raw_opex)
    df_capex = pd.DataFrame(raw_capex)

    for df, nome in [(df_opex, "opex"), (df_capex, "capex")]:
        df["_ingested_at"] = TIMESTAMP
        df["_source"] = "Sistema_Financeiro_simulado"
        df["_layer"] = "bronze"
        path = os.path.join(RAW_DIR, f"{nome}_raw.csv")
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"  -> Salvo: {path} ({len(df)} registros)")

    return df_opex, df_capex


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def run():
    print("=" * 60)
    print("PRIME D'OR | Pipeline de Dados RH")
    print("Camada BRONZE — Ingestão Raw")
    print(f"Timestamp: {TIMESTAMP}")
    print("=" * 60)

    df_mov  = ingest_movimentacao_hris()
    df_sal  = ingest_pesquisa_salarial()
    df_play = ingest_benchmarks_players()
    df_opex, df_capex = ingest_orcamento()

    # Manifesto de ingestão
    manifest = {
        **META,
        "datasets": {
            "movimentacao_hris": {"registros": len(df_mov),  "path": "bronze/movimentacao_hris_raw.csv"},
            "pesquisa_salarial": {"registros": len(df_sal),  "path": "bronze/pesquisa_salarial_raw.csv"},
            "benchmarks_players":{"registros": len(df_play), "path": "bronze/benchmarks_players_raw.csv"},
            "opex":              {"registros": len(df_opex), "path": "bronze/opex_raw.csv"},
            "capex":             {"registros": len(df_capex),"path": "bronze/capex_raw.csv"},
        }
    }
    manifest_path = os.path.join(RAW_DIR, f"_manifest_{TIMESTAMP}.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print("=" * 60)
    print(f"[BRONZE] Ingestao concluida. Manifesto: {manifest_path}")
    print("Proxima etapa: executar 02_silver_tratamento.py")
    print("=" * 60)


if __name__ == "__main__":
    run()
