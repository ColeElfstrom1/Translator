from random import random

cost = 2
roi = 0.97

prize_multipliers = [1, 2, 5, 10, 20, 50, 100]
prizes = [cost * multiplier for multiplier in prize_multipliers]
prize_odds = [roi / (multiplier * len(prize_multipliers)) for multiplier in prize_multipliers]

prize_gates = len(prize_multipliers) * [0]
for a in range(len(prize_gates)):
    prize_gates[a] = prize_gates[a - 1] + prize_odds[-a - 1]

def spin_slot():
    global balance

    if balance < cost:
        print("Ran out money. Aw dangit.")
        return

    balance -= cost
    spin_value = random()

    for a in range(len(prize_gates)):
        if spin_value <= prize_gates[a]:
            balance += prizes[len(prizes) - a - 1]
            print(f"Congratulations! You won ${prizes[len(prizes) - a - 1]}!\nYour balance is now ${balance}.")
            return

    print(f"Try again!\nYour balance is now ${balance}.")

balance = 1000

for a in range(0,10000):
    spin_slot()
    
    if balance == 0:
        print(a)
        break
