# Suits: 0:clubs, 1:diamonds, 2:hearts, 3:spades
class Card:
    suit_list = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_list = ['narf', 'Ace', '2', '3', '4', '5', '6',
                 '7', '8', '9', '10', 'Jack', 'Queen', 'King']
    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank
    def __str__(self):
        return (self.rank_list[self.rank] + ' of ' +
                self.suit_list[self.suit])
    def __cmp__(self, other):
        # check the suits
        if self.suit > other.suit: return 1
        if self.suit < other.suit: return -1
        # suits are the same -> check ranks
        if self.rank > other.rank: return 1
        if self.rank < other.rank: return -1
        # ranks are the same -> tie
        return 0


class Deck:
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1,14):
                self.cards.append(Card(suit, rank))
    def __str__(self):
        s = ''
        for i in range(len(self.cards)):
            s = s + ' '*i + str(self.cards[i]) + '\n'
        return s
    def shuffle(self):
        import random
        n_cards = len(self.cards)
        for i in range(n_cards):
            j = random.randrange(i, n_cards)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]
    def remove_card(self, card):
        if card in self.cards:
            self.cards.remove(card)
            return True
        else:
            return False
    def pop_card(self):
        return self.cards.pop()    # pop: removing the last element in a list
    def is_empty(self):
        return (len(self.cards) == 0)
    def deal(self, hands, n_cards=999):
        n_hands = len(hands)
        for i in range(n_cards):
            if self.is_empty(): break    # break if out of cards
            card = self.pop_card()       # take the top card
            hand = hands[i % n_hands]    # whose turn is next?
            hand.add_card(card)          # add the card to the hand


class Hand(Deck):
    def __init__(self, name=''):
        self.cards = []
        self.name = name
    def __str__(self):
        s = 'Hand ' + self.name
        if self.is_empty():
            return s + ' is empty\n'
        else:
            return s + ' contains\n' + Deck.__str__(self)
    def add_card(self, card):
        self.cards.append(card)


class CardGame:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()


class OldMaidHand(Hand):
    def remove_matches(self):
        count = 0
        original_cards = self.cards[:]
        for card in original_cards:
            match = Card(3 - card.suit, card.rank)
            # 3 - card.suit turns a suit 0/1 into a suit 3/2
            print(match)
            print(self.cards)
            if match in self.cards:    # TODO match is not in self.cards
                self.cards.remove(card)
                self.cards.remove(match)
                print('Hand %s: %s matches %s' %(self.name,card,match))
                count = count + 1
        return count


class OldMaidGame(CardGame):
    def play(self, names):
        # remove Queen of Clubs
        self.deck.remove_card(Card(0,12))
        # make a hand for each player
        self.hands = []
        for name in names:
            self.hands.append(OldMaidHand(name))
        # deal the cards
        self.deck.deal(self.hands)
        print('---------- Cards have been dealt')
        self.print_hands()
        # remove initial matches
        matches = self.remove_all_matches()
        print('---------- Matches discarded, play begins')
        self.print_hands()
        # play until all 50 cards are matched
        turn = 0
        num_hands = len(self.hands)
        while matches < 25:
            matches = matches + self.play_one_turn(turn)
            turn = (turn + 1) % num_hands
        print('---------- Game is Over')
        self.print_hands()
    def remove_all_matches(self):
        count = 0
        for hand in self.hands:
            count = count + hand.remove_matches()
        return count
    def play_one_turn(self, i):
        if self.hands[i].is_empty():
            return 0
        neighbor = self.find_neighbor(i)
        picked_card = self.hands[neighbor].pop_card()
        self.hands[i].add_card(picked_card)
        print('hand', self.hands[i].name, 'picked', picked_card)
        count = self.hands[i].remove_matches()
        self.hands[i].shuffle()
        return count
    def find_neighbor(self, i):
        num_hands = len(self.hands)
        for next in range(1, num_hands):
            neighbor = (i + next) % num_hands
            if not self.hands[neighbor].is_empty():
                return neighbor








# card1 = Card(suit=1, rank=11)
# card2 = Card(suit=1, rank=3)

# print(card1)
# print(card2)
# print(card1.__cmp__(card2))

# deck = Deck()
# deck.shuffle()
# hand = Hand('kw')
# deck.deal([hand], 5)
# print(hand)


game = CardGame()
hand = OldMaidHand('kw')
game.deck.deal([hand], 13)
print(hand)

hand.remove_matches()
print(hand)
