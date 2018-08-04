from poker import Card, Hand, Deck

# test single card
card_1 = Card('AS')
card_2 = Card('AD')
card_3 = Card('KS')
assert card_1 == card_2
assert card_1 != card_3
assert card_1 > card_3
assert not card_1 < card_3

# test comparing two poker hands
hand_1 = Hand('AS 2D 4C 7H KS')
hand_2 = Hand('AC 2C 4D 7S KH')
assert hand_1 == hand_2
assert hand_2 == hand_1

hand_1 = Hand('AS 2D 4C 7H KS')
hand_2 = Hand('QS 3D 5C 8H 10S')
assert hand_1 > hand_2
assert hand_2 < hand_1

hand_1 = Hand('2H 3D 4S 9C KD')
hand_2 = Hand('2H 3D 6S 8C KD')
assert hand_1 > hand_2
assert hand_2 < hand_1

# test comparing all valid hand types
royal_flush      = Hand('AS 10S JS QS KS')
straight_flush_1 = Hand('AS 2S 3S 4S 5S')
straight_flush_2 = Hand('6S 2S 3S 4S 5S')
flush            = Hand('AS 2S 3S 4S 6S')
four_kind        = Hand('AS AC AD AH 5S')
full_house       = Hand('AS AC AD 5H 5S')
straight_1       = Hand('AH 2S 3S 4S 5S')
straight_2       = Hand('6S 2D 3S 4S 5S')
three_kind       = Hand('AS AC AD 4H 5S')
two_pair         = Hand('AS AC 4D 4H 5S')
pair             = Hand('AS 2C 4D 4H 5S')
high_card_1      = Hand('AS 2C 4D 7H 5S')
high_card_2      = Hand('9S 2C 4D 7H 5S')
assert royal_flush.hand == 'royal flush'
assert straight_flush_1.hand == straight_flush_2.hand == 'straight flush'
assert flush.hand == 'flush'
assert straight_1.hand == straight_2.hand == 'straight'
assert four_kind.hand == 'four of a kind'
assert full_house.hand == 'full house'
assert three_kind.hand == 'three of a kind'
assert two_pair.hand == 'two pair'
assert pair.hand == 'pair'
assert high_card_1.hand == high_card_2.hand == 'high card'

assert (
    royal_flush
    > straight_flush_1
    > straight_flush_2
    > four_kind
    > full_house
    > flush
    > straight_1
    > straight_2
    > three_kind
    > two_pair
    > pair
    > high_card_1
    > high_card_2
)

# test creating a deck
deck = Deck()
assert len(deck) == 52
assert all(isinstance(card, Card) for card in deck)

# test creating a hand from the deck
hand_1 = Hand(deck)
hand_2 = Hand(deck)
assert len(hand_1) == 5
assert len(hand_2) == 5
