import yfinance as yf
import pandas as pd
import time
import os

print("Iniciando a busca de metadados dos ativos...")

# Garante a pasta de saída
os.makedirs('dados', exist_ok=True)

def ler_arquivo_b3(nome_arquivo):
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

# Base de ações e fundos
df_ibov = ler_arquivo_b3('dados/dim_ibovespa_assets.csv').assign(Categoria='Ação')
df_ifix = ler_arquivo_b3('dados/dim_ifix_assets.csv').assign(Categoria='Fundo')

# Junta e remove duplicados
df_ativos_base = pd.concat([df_ibov, df_ifix], ignore_index=True).drop_duplicates(subset=['Codigo'])

dados_extraidos = []

for i, row in enumerate(df_ativos_base.itertuples(index=False), start=1):
    ticker = row.Codigo
    categoria = row.Categoria
    simbolo = f"{ticker}.SA"

    try:
        print(f"[{i}/{len(df_ativos_base)}] Consultando: {simbolo}")

        info = yf.Ticker(simbolo).info or {}

        nome_empresa = info.get('longName') or info.get('shortName') or ticker
        nome_curto = info.get('shortName') or ticker

        if categoria == 'Fundo':
            setor_padrao = 'Fundo Imobiliário'
            industria_padrao = 'Imobiliário'
            tipo_papel = 'FII'
        else:
            setor_padrao = 'Outros'
            industria_padrao = 'Outros'

            if ticker.endswith('3'):
                tipo_papel = 'ON'
            elif ticker.endswith('4'):
                tipo_papel = 'PN'
            elif ticker.endswith('11'):
                tipo_papel = 'UNT'
            else:
                tipo_papel = 'Outro'

        setor = info.get('sector') or setor_padrao
        industria = info.get('industry') or industria_padrao

        dados_extraidos.append({
            'Codigo': ticker,
            'Empresa': nome_empresa,
            'Nome_Curto': nome_curto,
            'Tipo_Papel': tipo_papel,
            'Setor': setor,
            'Industria': industria
        })

    except Exception as e:
        print(f"Erro ao buscar {simbolo}: {e}")

        if categoria == 'Fundo':
            setor_erro = 'Fundo Imobiliário'
            industria_erro = 'Imobiliário'
            tipo_papel = 'FII'
        else:
            setor_erro = 'N/A'
            industria_erro = 'N/A'

            if ticker.endswith('3'):
                tipo_papel = 'ON'
            elif ticker.endswith('4'):
                tipo_papel = 'PN'
            elif ticker.endswith('11'):
                tipo_papel = 'UNT'
            else:
                tipo_papel = 'Outro'

        dados_extraidos.append({
            'Codigo': ticker,
            'Empresa': ticker,
            'Nome_Curto': ticker,
            'Tipo_Papel': tipo_papel,
            'Setor': setor_erro,
            'Industria': industria_erro
        })

    time.sleep(0.5)

# Cria DataFrame com os dados enriquecidos
df_info_extra = pd.DataFrame(dados_extraidos)

# Merge com a base original
df_final = pd.merge(df_ativos_base, df_info_extra, on='Codigo', how='left')
df_final.rename(columns={'Codigo': 'Ticker'}, inplace=True)

# Preenche valores faltantes
df_final['Empresa'] = df_final['Empresa'].fillna(df_final['Ticker'])
df_final['Nome_Curto'] = df_final['Nome_Curto'].fillna(df_final['Ticker'])
df_final['Tipo_Papel'] = df_final['Tipo_Papel'].fillna('Outro')
df_final['Setor'] = df_final['Setor'].fillna('N/A')
df_final['Industria'] = df_final['Industria'].fillna('N/A')

# Salva a dimensão final
df_final.to_csv('dados/dim_ativos_B3.csv', index=False, encoding='utf-8-sig')

print("Arquivo gerado com sucesso: dados/dim_ativos_B3.csv")