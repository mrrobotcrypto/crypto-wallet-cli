import json
import os
from wallet import generate_wallet

WALLET_FILE = "wallets.json"


def load_wallets():
    """Load existing wallets from file."""
    if os.path.exists(WALLET_FILE):
        with open(WALLET_FILE, "r") as f:
            return json.load(f)
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


def main_menu():
    """Interactive CLI menu."""
    wallets = load_wallets()
    while True:
        print("\n=== 🪙 CRYPTO WALLET CLI ===")
        print("1️⃣  Generate new wallet")
        print("2️⃣  List saved wallets")
        print("3️⃣  Export all wallets (JSON)")
        print("4️⃣  Exit")

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
            print(json.dumps(wallets, indent=4))
        elif choice == "4":
            print("\n👋 Goodbye, MrRobotCrypto!")
            break
        else:
            print("⚠️ Invalid selection, please try again.")


if __name__ == "__main__":
    main_menu()
