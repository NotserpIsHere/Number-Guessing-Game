import random
import time

def play_game(difficulty, multiplayer=False, sequence=False, cooperative=False, points=0):
    if difficulty == "custom":
        number_range = int(input("Enter the maximum possible number: "))
        max_guesses = int(input("Enter the maximum number of guesses: "))
        if sequence:
            sequence_length = int(input("Enter the length of the sequence: "))
            numbers = [random.randint(1, number_range) for _ in range(sequence_length)]
        else:
            number = random.randint(1, number_range)
    elif difficulty == "easy":
        max_guesses = 10
        if sequence:
            numbers = [random.randint(1, 10) for _ in range(3)]
        else:
            number = random.randint(1, 100)
    elif difficulty == "medium":
        max_guesses = 8
        if sequence:
            numbers = [random.randint(1, 50) for _ in range(4)]
        else:
            number = random.randint(1, 500)
    else:
        max_guesses = 5
        if sequence:
            numbers = [random.randint(1, 100) for _ in range(5)]
        else:
            number = random.randint(1, 1000)

    if multiplayer:
        players = int(input("Enter the number of players: "))
        scores = [0] * players
        powerups = [0] * players
    else:
        players = 1
        scores = [0]
        powerups = [0]

    for i in range(max_guesses):
        for j in range(players):
            start_time = time.time()
            if sequence:
                print(f"Player {j+1}, enter your guesses separated by spaces: ")
                guesses = list(map(int, input().split()))
            else:
                guess = int(input(f"Player {j+1}, enter your guess: "))
            end_time = time.time()
            if end_time - start_time > 10:
                print("Sorry, you took too long to guess.")
                continue
            scores[j] += 1
            if sequence:
                correct = 0
                for k in range(len(numbers)):
                    if guesses[k] < numbers[k]:
                        print(f"Your guess for number {k+1} is too low.")
                    elif guesses[k] > numbers[k]:
                        print(f"Your guess for number {k+1} is too high.")
                    else:
                        correct += 1
                if correct == len(numbers):
                    print(f"Congratulations Player {j+1}! You guessed all the numbers in {scores[j]} tries.")
                    return
                elif correct > 0:
                    print(f"You have {correct} correct guesses.")
            else:
                if guess < number:
                    print("Your guess is too low.")
                elif guess > number:
                    print("Your guess is too high.")
                else:
                    print(f"Congratulations Player {j+1}! You guessed the number in {scores[j]} tries.")
                    return

            powerup_chance = random.random()
            if powerup_chance < 0.2:
                powerups[j] += 1
                print(f"Player {j+1}, you got a power-up! You can use it to get a hint or an extra guess.")

            use_powerup = input(f"Player {j+1}, do you want to use a power-up (yes/no): ") == "yes"
            if use_powerup and powerups[j] > 0:
                powerups[j] -= 1
                powerup_type = input("Choose power-up type (hint/extra guess): ")
                if powerup_type == "hint":
                    if sequence:
                        hint_index = random.randint(0, len(numbers)-1)
                        print(f"The number at position {hint_index+1} is {numbers[hint_index]}.")
                    else:
                        hint_range = (number - guess) // 2
                        hint_number = random.randint(number-hint_range, number+hint_range)
                        print(f"The number is within {hint_range} of {hint_number}.")
                else:
                    i -= 1

            use_hint = input(f"Player {j+1}, do you want to use a hint (yes/no): ") == "yes"
            if use_hint and points >= 10:
                points -= 10
                if sequence:
                    hint_index = random.randint(0, len(numbers)-1)
                    print(f"The number at position {hint_index+1} is {numbers[hint_index]}.")
                else:
                    hint_range = (number - guess) // 2
                    hint_number = random.randint(number-hint_range, number+hint_range)
                    print(f"The number is within {hint_range} of {hint_number}.")
            elif use_hint and points < 10:
                print(f"Sorry, you don't have enough points to use a hint. You need 10 points and you only have {points}.")

        if cooperative and sequence:
            all_correct = True
            for k in range(len(numbers)):
                correct = False
                for j in range(players):
                    if guesses[j][k] == numbers[k]:
                        correct = True
                        break
                if not correct:
                    all_correct = False
                    break
            if all_correct:
                print(f"Congratulations! You all worked together to guess the sequence in {i+1} rounds.")
                return

    if sequence:
        print(f"Sorry, you all ran out of guesses. The correct numbers were {numbers}.")
    else:
        print(f"Sorry, you all ran out of guesses. The correct number was {number}.")

    return points

difficulty = input("Choose difficulty (easy, medium, hard, custom): ")
multiplayer = input("Multiplayer mode (yes/no): ") == "yes"
sequence = input("Sequence mode (yes/no): ") == "yes"
cooperative = input("Cooperative mode (yes/no): ") == "yes"
points = 0
while True:
    play_again = input("Do you want to play again (yes/no): ") == "yes"
    if not play_again:
        break
    points = play_game(difficulty, multiplayer, sequence, cooperative, points)
    points += 10