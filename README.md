# Painel de Inclusao Digital - Sitio Cercado (Curitiba/PR)

Projeto da **Atividade Extensionista II - Tecnologia Aplicada a Inclusao Digital**
do CST em **Ciencia de Dados** (UNINTER).

Autor: **Kaiky Santos Ribeiro** | RU: 4683386

## O problema

O telecentro comunitario mantido por uma associacao de moradores no bairro
Sitio Cercado, em Curitiba/PR, oferece oficinas gratuitas de informatica, mas
nao tinha uma forma organizada de **saber quais habilidades digitais faltam**
aos moradores. As turmas eram montadas "no achismo".

## A solucao

Um painel interativo (dashboard) em **Python** que le as respostas de um
questionario aplicado na comunidade, calcula indicadores com **Pandas** e
mostra graficos com **Streamlit/Altair**, permitindo aos monitores
**priorizar as oficinas** pelas maiores lacunas de habilidade.

## Tecnologias

- Python 3.10+
- Pandas (tratamento e analise dos dados)
- Streamlit (interface web do painel)
- Altair (graficos)

## Como executar

```bash
# 1. instalar dependencias
pip install -r requirements.txt

# 2. gerar a base de exemplo (dados ficticios)
python gerar_dados.py

# 3. rodar o painel
streamlit run app.py
```

O painel abre no navegador em `http://localhost:8501`.

## Estrutura

```
painel-inclusao-digital/
├── app.py                 # aplicativo Streamlit (o painel)
├── gerar_dados.py         # gera a base de exemplo em dados/
├── dados/
│   └── respostas_comunidade.csv   # respostas do questionario
├── requirements.txt
├── README.md
└── .gitignore
```

## O questionario

Cada linha do CSV e um respondente do telecentro. Colunas:

| Coluna | Descricao |
|---|---|
| id | identificador |
| faixa_etaria | 15-24, 25-39, 40-59, 60+ |
| genero | Feminino / Masculino |
| escolaridade | nivel de estudo |
| tem_internet_casa | Sim / Nao |
| dispositivo_principal | Smartphone / Computador / Tablet / Nenhum |
| ligar_e_usar_computador | habilidade (0 a 3) |
| navegar_internet | habilidade (0 a 3) |
| enviar_email | habilidade (0 a 3) |
| usar_apps_gov_br | habilidade (0 a 3) |
| buscar_emprego_online | habilidade (0 a 3) |
| seguranca_senhas | habilidade (0 a 3) |
| interesse_oficina | oficina de maior interesse |

Escala de habilidade: **0** = nao sabe, **1** = com muita ajuda,
**2** = com pouca ajuda, **3** = faz sozinho.

> Os dados deste repositorio sao ficticios, apenas para demonstracao.
> Em uso real, o CSV e substituido pelas respostas coletadas na comunidade.

## Licenca

MIT
