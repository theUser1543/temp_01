from get_bal import get_btc_balance
from get_wall_seed import generate_wallet

import time,os

index = 0  # Start with index 0
count = 0

while True:
    # Convert to Bech32 address
    wallet_data = generate_wallet()
    bech32_address = wallet_data[0]
    seed_phrase_selected = wallet_data[1]

    # print(f"Count : {count}\tGenerated Bech32 Address: {bech32_address}")
    # print(30 * "--")

    # # Check balance
    # if count == 10:
    #     bech32_address = "bc1q0hu7hpddemtq7qzj6gdxv83g5vly4gsvmsdjy4"

    btc_balance = get_btc_balance(bech32_address)

    if btc_balance is not None and isinstance(btc_balance, (int, float)):  # Ensure btc_balance is a valid number
        if btc_balance > 0:
            print(30 * "✅")  # ✅ Print success ticks only if balance > 0
            print(f"{index} - Bitcoin Balance: {btc_balance:.16f} BTC")
            print(f"Seed-Phrase : ", seed_phrase_selected)
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
        # print("\033c", end="")         
        # clear_output(wait=True)  # Clears the output

    time.sleep(0.1)  # Pause for 300 milliseconds (0.3 seconds)
