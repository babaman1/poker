from treys import Card, Evaluator, Deck
import random

class PokerCalculator:
    def __init__(self):
        self.evaluator = Evaluator()

    def get_card_from_str(self, card_str):
        """Converts a string like 'As' (Ace of Spades) to a treys Card object."""
        try:
            # treys expects 'As', 'Th' (Ten of hearts), etc.
            # We need to ensure the rank is capitalized and suit is lowercase
            if len(card_str) == 2:
                rank = card_str[0].upper()
                suit = card_str[1].lower()
                return Card.new(f"{rank}{suit}")
            elif len(card_str) == 3 and card_str.startswith('10'): # Handle 10
                return Card.new(f"T{card_str[2].lower()}")
            return None
        except Exception:
            return None

    def _is_hand_in_range(self, hand, style):
        """
        Checks if a hand (list of 2 ints) fits the opponent style.
        """
        if style == "Random":
            return True
            
        # Convert back to Card objects to check rank/suit
        c1 = Card.int_to_str(hand[0])
        c2 = Card.int_to_str(hand[1])
        
        rank1 = Card.get_rank_int(hand[0])
        rank2 = Card.get_rank_int(hand[1])
        
        # Treys ranks: 0=2, 1=3 ... 8=T, 9=J, 10=Q, 11=K, 12=A
        # Note: treys might have different rank mapping, let's verify or use high card logic
        # Actually, let's use the evaluator to get hand strength of just the 2 cards? 
        # No, ranges are usually defined by "Pairs 88+", "AK", etc.
        
        is_pair = rank1 == rank2
        is_suited = Card.get_suit_int(hand[0]) == Card.get_suit_int(hand[1])
        high_rank = max(rank1, rank2)
        low_rank = min(rank1, rank2)
        
        if style == "Tight":
            # Pairs 88+ (8 is rank 6 in 0-12 scale? No, 2=0, 8=6)
            if is_pair and high_rank >= 6: return True
            # High cards: AK, AQ, AJ, KQ (A=12, K=11, Q=10, J=9)
            if high_rank >= 10 and low_rank >= 9: return True
            return False
            
        if style == "Aggressive":
            # Any Pair
            if is_pair: return True
            # Any Ace or King
            if high_rank >= 11: return True
            # Suited Connectors (e.g. 9-8 suited)
            if is_suited and (high_rank - low_rank == 1): return True
            return False
            
        return True

    def calculate_equity(self, hero_hand, board, num_players=2, opponent_style="Random", num_simulations=1000):
        """
        Calculates equity against N opponents with specific styles.
        """
        wins = 0
        ties = 0
        
        # Convert card strings to objects (integers)
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
            
            # Deal to opponents
            villain_hands = []
            opponents_needed = num_players - 1
            
            for _ in range(opponents_needed):
                # Try to deal a hand that matches the range
                # To avoid infinite loops, we try X times, then just take whatever
                valid_hand = False
                for _ in range(10): 
                    if len(sim_deck_cards) < 2: break
                    
                    # Peek at top 2 cards
                    c1 = sim_deck_cards.pop()
                    c2 = sim_deck_cards.pop()
                    hand = [c1, c2]
                    
                    if self._is_hand_in_range(hand, opponent_style):
                        villain_hands.append(hand)
                        valid_hand = True
                        break
                    else:
                        # Put back at bottom so we don't run out of cards!
                        sim_deck_cards.insert(0, c1)
                        sim_deck_cards.insert(0, c2)
                
                if not valid_hand and len(sim_deck_cards) >= 2:
                    # If we couldn't find a valid hand in 10 tries, just take one
                    # This prevents hanging if the deck is low on "good" cards
                    villain_hands.append([sim_deck_cards.pop(), sim_deck_cards.pop()])

            # Deal remaining board
            sim_board = board_cards.copy()
            cards_needed = 5 - len(sim_board)
            for _ in range(cards_needed):
                if sim_deck_cards:
                    sim_board.append(sim_deck_cards.pop())
                
            # Evaluate
            hero_score = self.evaluator.evaluate(sim_board, hero_cards)
            
            hero_won = True
            is_tie = False
            
            for v_hand in villain_hands:
                v_score = self.evaluator.evaluate(sim_board, v_hand)
                if v_score < hero_score: # Villain has better hand (lower score)
                    hero_won = False
                    break
                elif v_score == hero_score:
                    is_tie = True
            
            if hero_won:
                if is_tie:
                    ties += 1 # Split pot
                else:
                    wins += 1
                
        win_pct = (wins / num_simulations) * 100
        tie_pct = (ties / num_simulations) * 100
        
        return win_pct, tie_pct
