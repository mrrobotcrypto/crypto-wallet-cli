import json
import os
import requests
import datetime

from wallet import generate_wallet

# === CONFIGURATION ===
WALLET_FILE = "wallets.json"
API_URL = "http://192.168.1.106:5000"  # blockchain-sim API endpoint


# === FILE MANAGEMENT ===
def load_wallets():
    """Load existing wallets from file."""
    if os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ Wallet file corrupted, starting fresh.")
                return []
    return []


def save_wallets(wallets):
    """Save wallet list to file."""
    with open(WALLET_FILE, "w") as f:
        json.dump(wallets, f, indent=4)


def list_wallets(wallets):
    """Display all saved wallets."""
    if not wallets:
        print("\n📭 No wallets found.")
        return
    print("\n💼 Saved Wallets:")
    for i, w in enumerate(wallets, start=1):
        print(f"{i}. Address: {w['address']}")


# === TRANSACTION FEATURE ===
def send_transaction():
    """Send a new transaction to the blockchain node."""
    print("\n=== 🚀 SEND TRANSACTION ===")
    sender = input("From address: ").strip()
    receiver = input("To address: ").strip()
    amount = input("Amount: ").strip()

    try:
        amount = float(amount)
        if amount <= 0:
            print("⚠️ Amount must be positive.")
            return
    except ValueError:
        print("⚠️ Invalid amount. Must be a number.")
        return

    data = {"from": sender, "to": receiver, "amount": amount}

    try:
        res = requests.post(f"{API_URL}/transactions/new", json=data)
        if res.status_code == 201:
            print(f"\n✅ Transaction added to mempool!")
            print(f"   {sender} → {receiver} | Amount: {amount}")
            log_transaction(sender, receiver, amount)
	print("🗒️  Transaction saved to local history log.")
	


            auto_mine = input("\n⛏️  Mine transaction now? (y/n): ").strip().lower()
            if auto_mine == "y":
                miner = input("Enter miner name (default: MrRobotCrypto): ").strip() or "MrRobotCrypto"
                mine_res = requests.get(f"{API_URL}/mine?miner={miner}")
                if mine_res.status_code == 200:
                    print("\n💎 Block mined successfully!")
                    print(mine_res.text)
                else:
                    print("⚠️ Mining request failed.")
            else:
                print("🕒 Transaction left in mempool (not mined yet).")

        else:
            print(f"❌ Failed to send transaction (status {res.status_code})")
            print(res.text)
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Network error: {e}")



# === MAIN MENU ===
def main_menu():
    """Interactive CLI menu."""
    wallets = load_wallets()

    while True:
        print("\n=== 🪙 CRYPTO WALLET CLI ===")
        print("1️⃣  Generate new wallet")
        print("2️⃣  List saved wallets")
        print("3️⃣  Check wallet balance (via blockchain-sim)")
        print("4️⃣  Export all wallets (JSON)")
        print("5️⃣  Send transaction to blockchain")
        print("6️⃣  Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            new_wallet = generate_wallet()
            wallets.append(new_wallet)
            save_wallets(wallets)
            print(f"\n✅ New wallet created and saved!")
            print(f"Address: {new_wallet['address']}")

        elif choice == "2":
            list_wallets(wallets)

        elif choice == "3":
            if not wallets:
                print("\n⚠️ No wallets to check balance for.")
                continue

            print("\n🔍 Checking balances from blockchain-sim...\n")
            for w in wallets:
                try:
                    res = requests.get(f"{API_URL}/balance/{w['address']}")
                    if res.status_code == 200:
                        data = res.json()
                        print(f"💰 Address: {w['address']}")
                        print(f"   Balance: {data['balance']} coins\n")
                    else:
                        print(f"❌ API error for {w['address']}: {res.status_code}")
                except requests.exceptions.RequestException:
                    print("⚠️ Unable to connect to blockchain API.")
                    break

        elif choice == "4":
            print("\n📤 Exported Wallets (JSON):\n")
            print(json.dumps(wallets, indent=4))

        elif choice == "5":
            send_transaction()

        elif choice == "6":
            print("\n👋 Goodbye, MrRobotCrypto!")
            break

        else:
            print("⚠️ Invalid selection, please try again.")


def log_transaction(sender, receiver, amount):
    """Save every transaction locally in transactions.log"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("transactions.log", "a") as f:
        f.write(f"[{timestamp}] {sender} -> {receiver} | {amount} coins\n")



# === ENTRY POINT ===
if __name__ == "__main__":
    main_menu()
