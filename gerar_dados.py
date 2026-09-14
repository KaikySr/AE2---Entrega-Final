"""
gerar_dados.py
------------------------------------------------------------
Gera a base de exemplo (dados sinteticos) do questionario de
inclusao digital aplicado no telecentro comunitario do bairro
Sitio Cercado (Curitiba/PR).

Uso:
    python gerar_dados.py

Saida:
    dados/respostas_comunidade.csv

Observacao: os dados sao FICTICIOS, criados apenas para
demonstrar o funcionamento do painel. Em uso real, este CSV
seria substituido pelas respostas coletadas na comunidade.
"""

import os
import random
import pandas as pd

random.seed(42)  # reprodutibilidade

N = 80  # numero de respondentes

FAIXAS = ["15-24", "25-39", "40-59", "60+"]
GENEROS = ["Feminino", "Masculino"]
ESCOLARIDADE = [
    "Fundamental incompleto",
    "Fundamental completo",
    "Medio incompleto",
    "Medio completo",
    "Superior",
]
DISPOSITIVOS = ["Smartphone", "Computador", "Tablet", "Nenhum"]

# Habilidades digitais avaliadas (escala 0 a 3):
#   0 = nao sabe / nunca fez
#   1 = faz com muita ajuda
#   2 = faz com pouca ajuda
#   3 = faz sozinho
HABILIDADES = [
    "ligar_e_usar_computador",
    "navegar_internet",
    "enviar_email",
    "usar_apps_gov_br",
    "buscar_emprego_online",
    "seguranca_senhas",
]

OFICINAS = [
    "Informatica basica",
    "Internet e e-mail",
    "Servicos publicos digitais (gov.br)",
    "Curriculo e emprego online",
    "Seguranca digital",
]


def nivel_por_faixa(faixa):
    """Idosos tendem a ter menor habilidade; jovens, maior (com ruido)."""
    base = {"15-24": 2.4, "25-39": 2.1, "40-59": 1.4, "60+": 0.7}[faixa]
    valor = round(random.gauss(base, 0.8))
    return max(0, min(3, valor))


linhas = []
for i in range(1, N + 1):
    faixa = random.choices(FAIXAS, weights=[0.22, 0.28, 0.30, 0.20])[0]
    genero = random.choices(GENEROS, weights=[0.58, 0.42])[0]

    p_internet = {"15-24": 0.75, "25-39": 0.65, "40-59": 0.5, "60+": 0.3}[faixa]
    tem_internet = "Sim" if random.random() < p_internet else "Nao"

    dispositivo = random.choices(DISPOSITIVOS, weights=[0.62, 0.18, 0.06, 0.14])[0]

    linha = {
        "id": i,
        "faixa_etaria": faixa,
        "genero": genero,
        "escolaridade": random.choice(ESCOLARIDADE),
        "tem_internet_casa": tem_internet,
        "dispositivo_principal": dispositivo,
    }
    for hab in HABILIDADES:
        linha[hab] = nivel_por_faixa(faixa)

    if dispositivo == "Nenhum":
        for hab in HABILIDADES:
            linha[hab] = min(linha[hab], 1)

    linha["interesse_oficina"] = random.choice(OFICINAS)
    linhas.append(linha)

df = pd.DataFrame(linhas)

os.makedirs("dados", exist_ok=True)
caminho = os.path.join("dados", "respostas_comunidade.csv")
df.to_csv(caminho, index=False, encoding="utf-8")
print("Gerado", caminho, "com", len(df), "respondentes e", df.shape[1], "colunas.")
