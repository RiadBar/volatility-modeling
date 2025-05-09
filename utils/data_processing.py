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
