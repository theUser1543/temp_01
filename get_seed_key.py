from mnemonic import Mnemonic
import random
def get_seed():
    lang = "english"
    mnemo = Mnemonic(lang)
    lst = range(1,6)
    choice = random.choice(lst)
    # Dictionary to map user choice to valid entropy values
    options = {
        1: 128,  # 12 words
        2: 160,  # 15 words
        3: 192,  # 18 words
        4: 224,  # 21 words
        5: 256   # 24 words
    }

    try:
        # choice = int(input("Enter your choice (1-5): "))
        # choice = 2

        if choice not in options:
            raise ValueError
    except ValueError:
        print("Invalid choice. Defaulting to 12 words.")
        choice = 1

    strength = options[choice]
    new_seed_phrase = mnemo.generate(strength=strength)

    # print(30*"--")
    # print("chocie : ",choice)
    # print("Seed :",new_seed_phrase)
    # print(f"Available seed phrase length: Chosen-lenght {choice}")

    # for key, value in options.items():
    #     print(f"{key}: {value // 32 * 3} words")  # Convert bits to words correctly
    # print(30*"--")


    # print("Seed-Phrase : ",new_seed_phrase)
    return new_seed_phrase

# # Example usage
# seed = get_seed(2)
# print("Generated Seed Phrase:\n\n", seed)
