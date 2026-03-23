import yfinance as yf
import pandas as pd
import time

print("Iniciando a busca de setores e indústrias... Isso pode levar alguns minutos.")

# Reaproveitando sua lógica de leitura
def ler_arquivo_b3(nome_arquivo):
    df = pd.read_csv(nome_arquivo, sep=';', encoding='latin1', header=None, usecols=[0], engine='python')
    df.columns = ['Codigo']
    df['Codigo'] = df['Codigo'].astype(str).str.strip()
    df = df[df['Codigo'].str.len().between(4, 6)]
    return df

# 1. Carrega a lista completa de ativos
df_ibov = ler_arquivo_b3('dados/dim_ibovespa_assets.csv')
df_ifix = ler_arquivo_b3('dados/dim_ifix_assets.csv')
lista_codigos = pd.concat([df_ibov, df_ifix], ignore_index=True)['Codigo'].unique()

dados_setores = []

# 2. Loop para consultar o Yahoo Finance um por um
for i, ticker in enumerate(lista_codigos):
    try:
        simbolo = ticker + ".SA"
        print(f"[{i+1}/{len(lista_codigos)}] Consultando: {simbolo}...")
        
        info = yf.Ticker(simbolo).info
        
        # Pega o setor e indústria (se não achar, coloca 'Não Informado')
        setor = info.get('sector', 'Fundo de Investimento' if '11' in ticker else 'Outros')
        industria = info.get('industry', 'Imobiliário' if '11' in ticker else 'Outros')
        nome_empresa = info.get('longName', ticker)

        dados_setores.append({
            'Codigo': ticker,
            'Empresa': nome_empresa,
            'Setor': setor,
            'Industria': industria
        })
        
    except Exception as e:
        print(f"Erro ao buscar {ticker}: {e}")
        dados_setores.append({'Codigo': ticker, 'Empresa': ticker, 'Setor': 'N/A', 'Industria': 'N/A'})

    # Pequena pausa para o Yahoo não bloquear seu IP
    time.sleep(0.2)

# 3. Salva o resultado
df_final = pd.DataFrame(dados_setores)
df_final.to_csv('dados/dim_setores.csv', index=False, encoding='utf-8-sig')

print("\nSucesso! O arquivo 'dados/dim_setores.csv' foi gerado.")