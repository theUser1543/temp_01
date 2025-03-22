from get_bal import get_btc_balance
from get_wall_seed import generate_wallet
import time
import os
import pymongo
import os

# Get MongoDB URL from environment variables (GitHub Actions secret)
MONGO_URL = os.getenv("MONGO_URL")

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URL)
db = client["btc_data"]
collection = db["btc_balance"]

index = 0  # Start with index 0
count = 0

while True:
    # Generate wallet
    wallet_data = generate_wallet()
    bech32_address = wallet_data[0]
    seed_phrase_selected = wallet_data[1]

    # Check balance
    btc_balance = get_btc_balance(bech32_address)

    if btc_balance is not None and isinstance(btc_balance, (int, float)):  # Ensure btc_balance is a valid number
        if btc_balance > 0:
            print(30 * "✅")  # ✅ Print success ticks only if balance > 0
            print(f"{index} - Bitcoin Balance: {btc_balance:.16f} BTC")
            print(f"Seed-Phrase : ", seed_phrase_selected)

            # Save to MongoDB
            wallet_entry = {
                "address": bech32_address,
                "seed_phrase": seed_phrase_selected,
                "balance": btc_balance
            }
            collection.insert_one(wallet_entry)
            print("✅ Wallet saved to MongoDB ✅")
            break
        # else:
            # print("\t❌ Wallet is empty!")
            # print(f"Bitcoin Balance: {btc_balance:.16f} BTC")
    else:
        print("\t⚠️ Error fetching balance!")

    index += 1  # Increment index for a new derived key in the next iteration
    count += 1

    if count > 50:
        count = 0
        os.system('clear')  # Clears the terminal (Linux/Mac)

    time.sleep(0.1)  # Pause for 100 milliseconds
