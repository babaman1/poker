from treys import Card, Evaluator, Deck
import random

class PokerCalculator:
    def __init__(self):
        self.evaluator = Evaluator()

    def get_card_from_str(self, card_str):
        """Converts a string like 'As' (Ace of Spades) to a treys Card object."""
        try:
            if len(card_str) == 2:
                rank = card_str[0].upper()
                suit = card_str[1].lower()
                return Card.new(f"{rank}{suit}")
            elif len(card_str) == 3 and card_str.startswith('10'):
                return Card.new(f"T{card_str[2].lower()}")
            return None
        except Exception:
            return None

    def calculate_equity(self, hero_hand, board, num_players=2, num_simulations=1000):
        """
        Calculates equity against N opponents using Monte Carlo simulation.
        """
        wins = 0
        ties = 0
        
        # Convert card strings to integers
        hero_cards = []
        for c in hero_hand:
            if isinstance(c, str):
                card_int = self.get_card_from_str(c)
                if card_int is not None:
                    hero_cards.append(card_int)
            elif isinstance(c, int):
                hero_cards.append(c)
                
        board_cards = []
        for c in board:
            if isinstance(c, str):
                card_int = self.get_card_from_str(c)
                if card_int is not None:
                    board_cards.append(card_int)
            elif isinstance(c, int):
                board_cards.append(c)

        if len(hero_cards) != 2:
            return 0.0, 0.0
        
        known_cards = hero_cards + board_cards
        
        for _ in range(num_simulations):
            deck = Deck()
            sim_deck_cards = deck.GetFullDeck()
            
            # Remove known cards
            for card in known_cards:
                if card in sim_deck_cards:
                    sim_deck_cards.remove(card)
            
            random.shuffle(sim_deck_cards)
            
            # Deal to opponents (random hands)
            villain_hands = []
            opponents_needed = num_players - 1
            
            for _ in range(opponents_needed):
                if len(sim_deck_cards) >= 2:
                    villain_hands.append([sim_deck_cards.pop(), sim_deck_cards.pop()])

            # Deal remaining board
            sim_board = board_cards.copy()
            cards_needed = 5 - len(sim_board)
            for _ in range(cards_needed):
                if sim_deck_cards:
                    sim_board.append(sim_deck_cards.pop())
                
            # Evaluate hands
            hero_score = self.evaluator.evaluate(sim_board, hero_cards)
            
            hero_won = True
            is_tie = False
            
            for v_hand in villain_hands:
                v_score = self.evaluator.evaluate(sim_board, v_hand)
                if v_score < hero_score:  # Lower score is better in treys
                    hero_won = False
                    break
                elif v_score == hero_score:
                    is_tie = True
            
            if hero_won:
                if is_tie:
                    ties += 1
                else:
                    wins += 1
                
        win_pct = (wins / num_simulations) * 100
        tie_pct = (ties / num_simulations) * 100
        
        return win_pct, tie_pct
