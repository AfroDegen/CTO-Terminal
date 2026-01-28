def get_solana_tokens():
    """
    Get trending Solana tokens from DexScreener
    No API key needed, public endpoint
    """
    try:
        response = requests.get(
            "https://api.dexscreener.com/latest/dex/tokens/So11111111111111111111111111111111111111112",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            tokens = []
            
            for pair in data.get('pairs', [])[:20]:  # Top 20 pairs
                tokens.append({
                    'address': pair.get('baseToken', {}).get('address'),
                    'symbol': pair.get('baseToken', {}).get('symbol'),
                    'volume': float(pair.get('volume', {}).get('h24', 0)),
                    'liquidity': float(pair.get('liquidity', {}).get('usd', 0))
                })
            
            return tokens
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []
