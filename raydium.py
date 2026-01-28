def extract_token_mints(tx):
    """
    Extract SPL token mints involved in a transaction.
    Returns a set of mint addresses.
    """
    mints = set()

    message = tx["transaction"]["message"]

    for ix in message["instructions"]:
        if ix.get("parsed"):
            parsed = ix["parsed"]

            if parsed.get("type") in ["transfer", "transferChecked", "mintTo"]:
                info = parsed.get("info", {})
                mint = info.get("mint")
                if mint:
                    mints.add(mint)

    return mints
