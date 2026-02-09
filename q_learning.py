import random
from blackjack import Blackjack

from settings import *

class AI():
    def __init__(self, alpha=0.05, epsilon_start=0.05, epsilon_end=0.05, gamma=0.9):
        self.q = dict()
        self.moves = ["hit", "stand"]
        self.alpha = alpha
        self.start_epsilon = epsilon_start
        self.end_epsilon = epsilon_end
        self.epsilon_decay = 0
        self.gamma = gamma
        
    def update(self, old_state, action, new_state, reward):
        # update q model based on action
        old = self.get_q_value(old_state, action)
        best_future = 0 if action == "stand" else self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        # get q value
        if (tuple(state), action) in list(self.q.keys()):
            return self.q[(tuple(state), action)]
        else:
            return 0

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        # update q value for specific pair based on formula
        self.q[(tuple(state), action)] = old_q + self.alpha * (reward + self.gamma *  future_rewards - old_q)

    def best_future_reward(self, state):
        # get best future reward
        actions = dict()
        for i in self.moves:
            actions[i] = self.get_q_value(tuple(state), i)

        return max(actions.items(), key=lambda item: item[1])[1]

    def choose_action(self, state, epsilon=True):

        # epsilon probability to explore
        if epsilon == True and random.random() < max(self.start_epsilon - self.epsilon_decay, self.end_epsilon):
            return random.choice(self.moves)
        
        actions = dict()

        # find most optimal move
        for i in self.moves:
            if i not in actions:
                actions[i] = self.get_q_value(tuple(state), i)

        return max(actions.items(), key=lambda item: item[1])[0]

    def get_state(self, state, dfc):
        state = [int(c) for c in state]
        return sum(state), any([c == 1 for c in state]) and sum(state) <= 11, int(dfc)

    def calc_wr(self, l, d, w):
        return 0 if (w + l) == 0 else w / (w + l)

    def train(self, iterations=1000000, logs=False):
        game_res = [0, 0, 0]

        for i in range(iterations):
            game = Blackjack([self], notif=logs)
            self.epsilon_decay += self.start_epsilon / (iterations / 2)

            full_log, winners = game.play(training=True)
            log = full_log[1]
            log.reverse()
            card_sum = sum(int(c) for c in log)
            has_stood = card_sum < 21
            won_round = winners[0]
            dfc = full_log[0][0]

            if has_stood:
                self.update(
                    self.get_state(log, dfc),
                    "stand",
                    None,
                    won_round
                )
            
            else:
                self.update(
                    self.get_state(log[1:], dfc),
                    "hit",
                    self.get_state(log, dfc),
                    won_round
                )

            for num in range(1, len(log) - 1):
                self.update(
                    self.get_state(log[num:], dfc),
                    "hit",
                    self.get_state(log[num-1:], dfc),
                    0
                )
            
            game_res[won_round + 1] += 1
            print(f"[TRAIN] Iteration {i+1} of {iterations} complete. Game value: {won_round}, win rate: {self.calc_wr(*game_res)*100:.2f}%")

    def test(self, iteration=10000, logs=False):
        game_res = [0, 0, 0]
        for i in range(iteration):
            game = Blackjack([self], notif=logs)

            _, winners = game.play(training=False)
            game_res[winners[0] + 1] += 1

            print(f"[TEST] Iteration {i+1} of {iteration} complete. Game value: {winners[0]}, win rate: {self.calc_wr(*game_res)*100:.2f}%")
        
        print("=" * 10)
        print(f"Testing complete | Wins: {game_res[2]} | Draws: {game_res[1]} | Loss: {game_res[0]}")

        
if __name__ == "__main__":
    a = AI(alpha=ALPHA, gamma=GAMMA, epsilon_start=START_EPSILON, epsilon_end=END_EPSILON)
    a.train(TRAIN_ITERATIONS)
    a.test(TEST_ITERATIONS)
    
    game = Blackjack(players=[a])
    game.play()
