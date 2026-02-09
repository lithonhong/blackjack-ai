from q_learning import AI
from blackjack import Blackjack
from settings import *

ai = AI(alpha=ALPHA, gamma=GAMMA, epsilon_start=START_EPSILON, epsilon_end=END_EPSILON)
ai.train(iterations=TRAIN_ITERATIONS)
ai.test(iteration=TEST_ITERATIONS)

track_record = [[0, 0, 0] for i in range(2)]
num_games = 0

def calc_wr(l, d, w):
    return 0 if (w + l) == 0 else w / (w + l)
"""
with open("log.txt", "w") as f:
    f.write(str(ai.q))
"""
while True:
    game = Blackjack([ai, "human"])
    _, winners = game.play()

    for num, i in enumerate(winners):
        track_record[num][i+1] += 1
    
    num_games += 1

    print("=" * 20)
    print(f"End of game {num_games}")
    print(f"Win rates | AI: {calc_wr(*track_record[0])*100:.2f}% | Human: {calc_wr(*track_record[1])*100:.2f}%")

    ans = None
    while ans not in ("1", "2"):
        print("Continue?")
        print("1: Yes")
        print("2: No")
        ans = input(">> ")
        print("-" * 10)

    if ans == "2":
        print("Ending program...")
        break
    
    elif ans == "1":
        print(f"Starting game {num_games+1}...")
    
    print("=" * 20)