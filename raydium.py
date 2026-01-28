# raydium.py

RAYDIUM_PROGRAM_ID = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"

def detect_raydium_activity(block: dict):
    """
    Scans a Solana block for Raydium program interactions.
    Returns a list of events with tx signature + token mints.
    """

    events = []

    if not block or "transactions" not in block:
        return events

    for tx in block["transactions"]:
        try:
            message = tx["transaction"]["message"]
            meta = tx.get("meta", {})
            account_keys = message.get("accountKeys", [])

            # Check if Raydium program is involved
            program_ids = [
                acc["pubkey"] for acc in account_keys
                if acc.get("pubkey")
            ]

            if RAYDIUM_PROGRAM_ID not in program_ids:
                continue

            # Extract token mints from postTokenBalances
            mints = []
            for bal in meta.get("postTokenBalances", []):
                mint = bal.get("mint")
                if mint:
                    mints.append(mint)

            events.append({
                "signature": tx["transaction"]["signatures"][0],
                "mints": list(set(mints))
            })

        except Exception:
            # Never crash the dashboard because of one bad tx
            continue

    return events