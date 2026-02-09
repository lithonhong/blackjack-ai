import random



class Blackjack():

    def __init__(self, players : list = ["human"], notif=True):

        for p in range(len(players)):
            if type(players[p]).__name__ != "AI":
                players[p] = "human"
                if not notif:
                    print("Detected human in game. Logs are re-enabled.")
                    notif = True
        

        self.num_players = len(players)
        self.players = players
        self.curr_turn = 0
        self.notif = notif
        self.new_round()
    
    class Card():
        def __init__(self, rank, suit):
            self.rank = rank
            self.value = min(rank, 10)
            self.suit = suit
            self.get_text()
        
        def __str__(self):
            return self.text

        def __repr__(self):
            return f"Card({self.rank}, {self.suit})"

        def __int__(self):
            return self.value
        
        def get_text(self):
            self.suit_text = "♠♥♦♣"[self.suit]

            if self.rank == 1:
                self.rank_text = "A"
            elif self.rank > 10:
                self.rank_text = "JQK"[self.rank - 11]
            else:
                self.rank_text = str(self.rank)
            
            self.text = self.rank_text + " " + self.suit_text
            return self.text

    def new_round(self):
        self.winners = None
        self.curr_turn = 0

        # initialise cards 
        self.cards = [self.Card(i//4+1, i%4) for i in range(52)]
        
        random.shuffle(self.cards)

        self.hands = list()
        for _ in range(self.num_players):
            dealing_hand = [self.draw_card(), self.draw_card()]
            while self.evaluate_hand(dealing_hand) == 21:
                dealing_hand = [self.draw_card(), self.draw_card()]
            self.hands.append(dealing_hand)

        if self.notif:
            print("Welcome to Blackjack")

    def next_player(self):
        if self.curr_turn < self.num_players - 1:
            self.curr_turn += 1
        else:
            raise ValueError
    
    def prompt_user_input(self):
        curr_hand = self.hands[self.curr_turn]
        
        print("-" * 10)
        print(f"Player {self.curr_turn + 1} (Human)")
        print(f"Your hand: {', '.join([str(i) for i in curr_hand])} (Sum: {self.evaluate_hand(curr_hand)})")

        print("1: Hit")
        print("2: Stand")
        return input(">> ")

    def draw_card(self):
        cards_drawn = self.cards[0]
        self.cards = self.cards[1:]
        return cards_drawn

    def evaluate_hand(self, hand):
        ace = any([int(i) == 1 for i in hand])
        card_sum = sum([int(i) for i in hand])
        
        if card_sum <= 11 and ace:
            card_sum += 10

        return card_sum

    def human_move(self):
        user_move = None

        while user_move not in ["1", "2"]:
            user_move = self.prompt_user_input()
        
        if user_move == "2":
            print(f"You stood at {self.evaluate_hand(self.hands[self.curr_turn])}.")
            
        if user_move == "1":
            new_card = self.draw_card()
            self.hands[self.curr_turn].append(new_card)

            card_sum = self.evaluate_hand(self.hands[self.curr_turn])

            print(f"You drew a {new_card}.")
            
            if card_sum > 21:
                print("You busted!")
                
            elif card_sum == 21:
                print("You hit 21!")
            
            else:
                return self.human_move()
        
        return self.hands[self.curr_turn]
    
    def ai_move(self):
        curr_ai = self.players[self.curr_turn]
        curr_hand = self.hands[self.curr_turn]

        if self.notif:
            print("-" * 10)
            print(f"Player {self.curr_turn + 1} (AI)")
            print(f"Your hand: {', '.join([str(i) for i in curr_hand])} (Sum: {self.evaluate_hand(curr_hand)})")

        act = curr_ai.choose_action((
            self.evaluate_hand(curr_hand),
            any([int(i) == 1 for i in curr_hand]),
            int(self.dealer_hand[0])
        ), epsilon=self.training)

        if act == "stand":
            if self.notif:
                print("AI finished its turn.")
                print(f"AI stood at {self.evaluate_hand(self.hands[self.curr_turn])}.")
        
        else:
            new_card = self.draw_card()
            self.hands[self.curr_turn].append(new_card)
            
            card_sum = self.evaluate_hand(self.hands[self.curr_turn])

            if self.notif:
                print(f"AI drew a {new_card}.")

            #if card_sum >= 21:
            #    print("AI finished its turn.")

            if card_sum > 21:
                if self.notif:
                    print("AI busted!")
                
            elif card_sum == 21:
                if self.notif:
                    print("AI hit 21!")
            
            else:
                return self.ai_move()
        
        return self.hands[self.curr_turn]

    def move(self):
        if self.players[self.curr_turn] == "human":
            return self.human_move()

        else:
            return self.ai_move()

    def dealer(self):
        dealer_hand = [self.draw_card(), self.draw_card()]

        if self.notif:
            print("-" * 10)
            print("Dealer")
            print(f"Dealer face-up card: {dealer_hand[0]}")

        while self.evaluate_hand(dealer_hand) <= 16:
            dealer_hand.append(self.draw_card())
            
        if self.notif:
            print("Dealer stopped drawing cards.")

        self.dealer_hand = dealer_hand

        return dealer_hand

    def get_winner(self):
        winners = list()
        dealer_sum = self.evaluate_hand(self.dealer_hand)

        if self.notif:
            print("-" * 10)
            print("Results:")
            print(f"Dealer: {', '.join([str(i) for i in self.dealer_hand])} (Sum: {dealer_sum})")

        for i in range(self.num_players):
            player_type = 'AI' if type(self.players[i]).__name__ == 'AI' else self.players[i]
            player_hand_sum = self.evaluate_hand(self.hands[i])
            
            if player_hand_sum <= 21:
                if dealer_sum > 21 or dealer_sum < player_hand_sum:
                    res = 1 # player wins
                
                elif dealer_sum == player_hand_sum:
                    res = 0 # player ties
                
                else:
                    res = -1  # player loses
            
            else:
                res = -1 # player busts

            winners.append(res)
            
            if self.notif:
                print(f"Player {i + 1} ({player_type}): {', '.join([str(i) for i in self.hands[i]])} (Sum: {player_hand_sum}) - {['lose', 'draw', 'win'][res+1]}")

        return winners

    def play(self, training=False):
        self.training = training
        game_log = [self.dealer()]

        for i in range(self.num_players):
            game_log.append(self.move())
            if i < self.num_players - 1:
                self.next_player()

        winner = self.get_winner()

        return game_log, winner
    

if __name__ == "__main__":
    Blackjack(["human"]).play()
