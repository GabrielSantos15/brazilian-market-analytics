import yfinance as yf
import pandas as pd
import time
import os

print("Iniciando a busca de setores e indústrias...")

# Garante a pasta de saída para os arquivos gerados
os.makedirs('dados', exist_ok=True)

def ler_arquivo_b3(nome_arquivo):
    # Lê apenas a coluna de código e aplica limpeza básica
    df = pd.read_csv(
        nome_arquivo,
        sep=';',
        encoding='latin1',
        header=None,
        usecols=[0],
        engine='python'
    )
    df.columns = ['Codigo']
    df['Codigo'] = df['Codigo'].astype(str).str.strip()
    df = df[df['Codigo'].str.len().between(4, 6)]
    df = df[df['Codigo'].str.isalnum()]
    df = df[~df['Codigo'].str.upper().str.contains("CÓDIGO|CODIGO", na=False)]
    return df

# Define a categoria de cada base para preservar o tipo de ativo
df_ibov = ler_arquivo_b3('dados/dim_ibovespa_assets.csv').assign(Categoria='Ação')
df_ifix = ler_arquivo_b3('dados/dim_ifix_assets.csv').assign(Categoria='Fundo')

# Junta os ativos e remove duplicidades por código
df_ativos_base = pd.concat([df_ibov, df_ifix], ignore_index=True).drop_duplicates(subset=['Codigo'])

dados_extraidos = []

# Enriquecimento de dados com consulta individual no Yahoo Finance
for i, row in enumerate(df_ativos_base.itertuples(index=False), start=1):
    ticker = row.Codigo
    categoria = row.Categoria
    simbolo = f"{ticker}.SA"

    try:
        print(f"[{i}/{len(df_ativos_base)}] Consultando: {simbolo}")

        info = yf.Ticker(simbolo).info or {}

        nome_empresa = info.get('longName') or info.get('shortName') or ticker

        # Define fallback por categoria quando faltam metadados no ativo
        if categoria == 'Fundo':
            setor_padrao = 'Fundo Imobiliário'
            industria_padrao = 'Imobiliário'
        else:
            setor_padrao = 'Outros'
            industria_padrao = 'Outros'

        setor = info.get('sector') or setor_padrao
        industria = info.get('industry') or industria_padrao

        dados_extraidos.append({
            'Codigo': ticker,
            'Empresa': nome_empresa,
            'Setor': setor,
            'Industria': industria
        })

    except Exception as e:
        print(f"Erro ao buscar {simbolo}: {e}")

        if categoria == 'Fundo':
            setor_erro = 'Fundo Imobiliário'
            industria_erro = 'Imobiliário'
        else:
            setor_erro = 'N/A'
            industria_erro = 'N/A'

        dados_extraidos.append({
            'Codigo': ticker,
            'Empresa': ticker,
            'Setor': setor_erro,
            'Industria': industria_erro
        })

    time.sleep(0.5)

# Consolida os dados consultados e combina com a base original
df_info_extra = pd.DataFrame(dados_extraidos)

df_final = pd.merge(df_ativos_base, df_info_extra, on='Codigo', how='left')
df_final.rename(columns={'Codigo': 'Ticker'}, inplace=True)

# Ajusta possíveis lacunas antes de exportar
df_final['Empresa'] = df_final['Empresa'].fillna(df_final['Ticker'])
df_final['Setor'] = df_final['Setor'].fillna('N/A')
df_final['Industria'] = df_final['Industria'].fillna('N/A')

df_final.to_csv('dados/dim_ativos_B3.csv', index=False, encoding='utf-8-sig')

print("Arquivo gerado com sucesso: dados/dim_ativos_B3.csv")