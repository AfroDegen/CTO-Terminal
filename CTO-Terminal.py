import os
import time
import requests

# Load RPC URL from environment variable
RPC_URL = os.getenv("SOLANA_RPC_URL")

if not RPC_URL:
    raise ValueError("Missing SOLANA_RPC_URL environment variable")

HEADERS = {
    "Content-Type": "application/json"
}

def fetch_current_slot():
    """
    Fetch the current Solana slot from the RPC endpoint.
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSlot",
        "params": []
    }

    try:
        response = requests.post(RPC_URL, json=payload, headers=HEADERS, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "result" in data:
            slot = data["result"]
            print(f"[OK] Current Solana slot: {slot}")
            return slot
        else:
            print("[WARN] Unexpected RPC response format:", data)

    except requests.exceptions.RequestException as e:
        print("[ERROR] RPC connection failed:", e)

    return None


def main():
    print("CTO Terminal — Solana live monitoring started")

    while True:
        fetch_current_slot()
        time.sleep(20)


if __name__ == "__main__":
    main()