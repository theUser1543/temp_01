import requests

def get_btc_balance(bech32_address):

    url = f"https://blockstream.info/api/address/{bech32_address}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            balance_satoshis = data.get("chain_stats", {}).get("funded_txo_sum", 0) - data.get("chain_stats", {}).get("spent_txo_sum", 0)
            balance_btc = balance_satoshis / 1e8  # Convert satoshis to BTC

            return balance_btc  # Return balance as float
        else:
            return -1.00  # Return 0.0 BTC if API call fails
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return 0.0  # Ensure function always returns a float
#
