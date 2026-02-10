# Blackjack AI

An implementation of reinforcement learning agent that learns to play Blackjack via Q-learning.
This project comprises a basic Blackjack engine, a Q-learning model, and a simple settings file for configurations.


## Features
```
[TRAIN] Iteration 1000000 of 1000000 complete. Game value: 1, win rate: 36.21%
[TEST] Iteration 1 of 10000 complete. Game value: 1, win rate: 100.00%
```

* **Blackjack engine**: Basic game rules with dealer logic (no surrendering, betting or splitting).
* **Q-learning model**: Reinforcement learning agent.
* **Interactive display**: Play alongside the AI in the same game.
* **Customisable settings**: Modify values to tweak how the agent learns.


## Installation

1. Ensure you have Python installed on your system. (Python 3.6 or higher)

2. Clone this repository to your local machine using the following command:

`git clone https://github.com/lithonhong/flappy-bird-ai.git`

3. Navigate to the project directory:
`cd flappy-bird-ai`

4. Install the `random` module (if you don't have it yet)
`pip install -r requirements.txt`


## Usage

### Running the program

1. Run `main.py` if you wish to play alongside the AI, or `q_learing.py` otherwise.
The AI should commence its training & testing.

2. If you ran `q_learning.py`, the AI should complete running by printing out a complete log of a game.

3. If you ran `main.py`, it will prompt you to input `1` or `2` into the terminal depending on the context.

### Program structure

| File            | Function   |
| --------------- | ---------- |
| `blackjack.py`  | Handles game logic. |
| `main.py`       | Main game loop, allowing the user to play alongside the AI. |
| `q_learning.py` | Reinforcement learning agent implementation. |


## Q-learning
Q-learning is a reinforcement learning algorithm that trains an agent by assigning values to state-action pairs,
without requiring a model of the environment (model-free).
Instead, the agent learns from past experiences by trying different actions and observe its results.

The Q in Q-learning refers to the function it computes: its expected reward, `Q(s, a)`, of an action (`a`) given a state (`s`). Said function is defined as such:

$$Q(s, a) \leftarrow Q(s, a) + \alpha (r + \gamma max(Q(s', a')) - Q(s, a))$$

where `α` is the learning rate, `γ` is the discount factor, and `r` is the reward. `s', a'` refers to the state/action pair of the next move.

There is a probability `ϵ` that the agent does not pick the move with the best Q value, instead explores a random move.

In this program, the state is a tuple of the player's hand value, the presence of a usable ace, and the dealer's face-up card. The action, on the other hand, is either to hit or to stand.


## Results
The agent is able to reach a 38% win rate with 1 million training iterations. This is still suboptimal compared to the 42% win rate similar programs have.

Generally, the agent is able to act rationally. It hits below 17, and stands at 19 and 20. The agent demonstrates interesting behaviours when its sum is 17 or 18. Since the dealer is likely to have a sum greater than 17 anyway, it opts to take a leap of faith by drawing another card, in hopes of getting a 21.


## Feedback
Feel free to suggest improvements by **opening an issue** in this repository!


## Credits
The model is largely based on CS50AI's Project 4 - Nim, albeit with major edits to improve the model and suit it for the design of this project.

