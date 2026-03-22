import yfinance as yf
import pandas as pd
import os

print("Iniciando rotina de extração...")

os.makedirs('dados', exist_ok=True)

def ler_arquivo_b3(nome_arquivo):
    df = pd.read_csv(nome_arquivo, sep=';', encoding='latin1', header=None, usecols=[0], engine='python')
    df.columns = ['Codigo']
    df['Codigo'] = df['Codigo'].astype(str).str.strip()
    df = df[df['Codigo'].str.len().between(4, 6)]
    df = df[df['Codigo'].str.isalnum()]
    df = df[~df['Codigo'].str.upper().str.contains("CÓDIGO|CODIGO", na=False)]
    return df

# 1. Lê e limpa os arquivos
df_ibov = ler_arquivo_b3('dados/dim_ibovespa_assets.csv')
df_ifix = ler_arquivo_b3('dados/dim_ifix_assets.csv')
df_ativos = pd.concat([df_ibov, df_ifix], ignore_index=True)
tickers_yahoo = [ticker + '.SA' for ticker in df_ativos['Codigo']]

# Adicionando os Benchmarks na nossa lista de extração
tickers_yahoo.append('^BVSP')     # Ibovespa
tickers_yahoo.append('XFIX11.SA') # ETF espelho do IFIX

# 2. Baixa os dados 
print(f"Baixando preços e dividendos de {len(tickers_yahoo)} ativos (incluindo IBOV e IFIX)...")
dados = yf.download(tickers_yahoo, start="2020-01-01", actions=True)

# --- BLOCO 1: TRATAMENTO DOS PREÇOS ---
dados.columns.names = ['Price', 'Codigo']
df_precos = dados.stack(level='Codigo').reset_index()

if 'Adj Close' not in df_precos.columns:
    df_precos['Adj Close'] = df_precos['Close']
df_precos['Adj Close'] = df_precos['Adj Close'].fillna(df_precos['Close'])

tabela_precos = df_precos[['Date', 'Codigo', 'Close', 'Adj Close']].copy()
tabela_precos.rename(columns={'Close': 'Preco_Normal', 'Adj Close': 'Preco_Ajustado'}, inplace=True)
tabela_precos = tabela_precos.dropna(subset=['Preco_Normal'])
tabela_precos['Date'] = tabela_precos['Date'].dt.tz_localize(None)
tabela_precos['Codigo'] = tabela_precos['Codigo'].str.replace('.SA', '', regex=False)

tabela_precos.to_csv('dados/f_historico_precos.csv', index=False)
print("1/2 - Arquivo dados/f_historico_precos.csv gerado com sucesso.")

# --- BLOCO 2: TRATAMENTO DOS DIVIDENDOS ---
if 'Dividends' in dados.columns.get_level_values('Price'):
    df_div = dados['Dividends'].stack().reset_index()
    df_div.columns = ['Date', 'Codigo', 'Valor_Dividendo']
    
    df_div = df_div[df_div['Valor_Dividendo'] > 0].copy()
    df_div['Date'] = df_div['Date'].dt.tz_localize(None)
    df_div['Codigo'] = df_div['Codigo'].str.replace('.SA', '', regex=False)
    
    df_div.to_csv('dados/f_dividendos.csv', index=False)
    print("2/2 - Arquivo dados/f_dividendos.csv gerado com sucesso!")
else:
    print("Nenhum dividendo encontrado para esses ativos no período.")

print("Rotina ETL concluída perfeitamente!")
