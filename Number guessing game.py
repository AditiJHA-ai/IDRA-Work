import random


def number_guessing_game():
    LOWER_BOUND = 1
    UPPER_BOUND = 100
    MAX_ATTEMPTS = 7

    secret_number = random.randint(LOWER_BOUND, UPPER_BOUND)

    print("WELCOME TO THE NUMBER GUESSING GAME")
    print(f"I'm thinking of a number between {LOWER_BOUND} and {UPPER_BOUND}.")
    print(f"You have {MAX_ATTEMPTS} attempts to guess it correctly.\n")

    attempts_used = 0
    guessed_correctly = False

    while attempts_used < MAX_ATTEMPTS and not guessed_correctly:
        attempts_left = MAX_ATTEMPTS - attempts_used
        print(f"Attempts remaining: {attempts_left}")

        try:
            user_input = input("Enter your guess: ")
            guess = int(user_input)
        except ValueError:
            print("Invalid input! Please enter a valid whole number.\n")
            continue

        if guess < LOWER_BOUND or guess > UPPER_BOUND:
            print(
                f"Please enter a number strictly within {LOWER_BOUND} and {UPPER_BOUND}.\n"
            )
            continue

        attempts_used += 1

        if guess < secret_number:
            print("Too low! Try a higher number.\n")
        elif guess > secret_number:
            print("Too high! Try a lower number.\n")
        else:
            guessed_correctly = True

    if guessed_correctly:
        print(
            f"Congratulations! You guessed the number {secret_number} in {attempts_used} attempt(s)!"
        )
    else:
        print(
            f"Game Over! You've run out of attempts. The secret number was {secret_number}."
        )


if __name__ == "__main__":
    number_guessing_game()
