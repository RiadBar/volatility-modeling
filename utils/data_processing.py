import pandas as pd
import numpy  as np
import yfinance as yf

def download_asset_data(ticker, start, end):
    """
    Télécharge les données Yahoo Finance pour un ticker.
    Utilise 'Adj Close' par défaut, nettoie les NaN, et renvoie un DataFrame propre.
    Retourne None si aucune donnée exploitable.
    """
    try:
        data = yf.download(ticker, start = start, end = end)

        if data.empty:
            print(f" Aucune donnee recue pour {ticker}")
            return None
        
        if "Adj Close" in data.columns:
            price_series = data["Adj Close"].dropna()
        elif "Close" in data.columns:
            price_series = data["Close"].dropna()
        
        clean_df = pd.DataFrame({"Price": price_series})
        return clean_df
   
    
    except Exception as e:
        print(f"Erreur lors du téléchargement de {ticker} : {e}")
        return None
    
def log_returns(price_series):
    return np.log(price_series / price_series.shift(1)).dropna()

def get_multiple_assets(tickers, start, end):
    """
    Télécharge les données Yahoo Finance pour plusieurs tickers.
    Utilise 'Adj Close' par défaut, nettoie les NaN, et renvoie un DataFrame propre
    avec une colonne par ticker.
    """
    try:
        data = yf.download(tickers, start=start, end=end)

        if data.empty:
            print("Aucune donnée reçue pour les tickers spécifiés.")
            return None

        if "Adj Close" in data:
            m_clean_df = data["Adj Close"].dropna(how="all")
        elif "Close" in data:
            m_clean_df = data["Close"].dropna(how="all")
        

        return m_clean_df

    except Exception as e:
        print(f"Erreur lors du téléchargement des actifs : {e}")
        return None
    from utils.data_processing import get_multiple_assets, compute_log_returns_multi
import matplotlib.pyplot as plt

# Paramètres
tickers = ["AAPL", "MSFT", "GOOGL"]
start_date = "2022-01-01"
end_date = "2023-12-31"

# 1. Télécharger les prix ajustés
prices = get_multiple_assets(tickers, start=start_date, end=end_date)

if prices is None:
    print("❌ Échec du téléchargement des données.")
    exit()

print("✅ Données récupérées :")
print(prices.head())

# 2. Calculer les log-returns
log_returns = log_returns(prices)
print("\n✅ Log-returns calculés :")
print(log_returns.head())

# 3. Vérifier s’il y a des valeurs manquantes
missing = log_returns.isna().sum()
print("\n🔍 Nombre de valeurs manquantes par actif dans les log-returns :")
print(missing)

# 4. Tracer les rendements log pour chaque actif
log_returns.plot(figsize=(12, 6), title="Log-Returns des actifs sélectionnés")
plt.xlabel("Date")
plt.ylabel("Log-Return")
plt.grid(True)
plt.tight_layout()
plt.show()
