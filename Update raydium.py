def detect_raydium_activity(block_data):
    events = []

    if "result" not in block_data or block_data["result"] is None:
        return events

    for tx in block_data["result"]["transactions"]:
        message = tx["transaction"]["message"]

        raydium_hit = False
        for ix in message["instructions"]:
            if ix.get("programId") == RAYDIUM_AMM_PROGRAM:
                raydium_hit = True
                break

        if raydium_hit:
            mints = extract_token_mints(tx)
            events.append({
                "signature": tx["transaction"]["signatures"][0],
                "mints": list(mints)
            })

    return events
