import json
import os
import requests
import time
from datetime import datetime

API_URL = "http://127.0.0.1:5000"
WALLET_FILE = "wallets.json"
LOG_FILE = "monitor.log"


def load_wallets():
    if not os.path.exists(WALLET_FILE):
        print("⚠️ No wallets file found.")
        return []
    with open(WALLET_FILE, "r") as f:
        return json.load(f)


def log_balance(address, balance):
    """Write balance info to log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {address} → Balance: {balance}\n")


def check_wallets(interval=10):
    """Continuously monitor all wallet balances."""
    wallets = load_wallets()
    if not wallets:
        print("⚠️ No wallets to monitor.")
        return

    print(f"\n🔍 Monitoring {len(wallets)} wallets every {interval} seconds...\n")
    try:
        while True:
            for w in wallets:
                address = w["address"]
                try:
                    res = requests.get(f"{API_URL}/balance/{address}")
                    if res.status_code == 200:
                        balance = res.json().get("balance", 0)
                        print(f"💰 {address}: {balance} coins")
                        log_balance(address, balance)
                    else:
                        print(f"❌ API error for {address}: {res.status_code}")
                except requests.exceptions.RequestException:
                    print("⚠️ Unable to reach blockchain API.")
            print("\n⏳ Waiting for next check...\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n🛑 Monitoring stopped manually.")
