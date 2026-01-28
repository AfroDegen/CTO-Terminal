import asyncio
import json
import websockets
from collections import deque
import time

RAYDIUM_PROGRAM = "675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8"
RPC_WSS = "wss://api.mainnet-beta.solana.com"

events = deque(maxlen=100)

async def listen():
    while True:
        try:
            async with websockets.connect(RPC_WSS, ping_interval=20) as ws:
                sub = {
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "logsSubscribe",
                    "params": [
                        {"mentions": [RAYDIUM_PROGRAM]},
                        {"commitment": "confirmed"}
                    ]
                }
                await ws.send(json.dumps(sub))

                while True:
                    msg = await ws.recv()
                    data = json.loads(msg)

                    if "params" not in data:
                        continue

                    value = data["params"]["result"]["value"]
                    logs = value.get("logs", [])
                    sig = value.get("signature")

                    for l in logs:
                        if (
                            "AddLiquidity" in l
                            or "InitializePool" in l
                            or "Deposit" in l
                        ):
                            events.appendleft({
                                "signature": sig,
                                "log": l,
                                "ts": time.time()
                            })

        except Exception as e:
            print("Raydium WS error:", e)
            time.sleep(3)